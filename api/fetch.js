const schedule = require("node-schedule")
const fetch = require("node-fetch")
const htmlParser = require("htmlparser2")
const DomHandler = require("domhandler")
const domUtils = require("domutils")
const htmlEntities = require("html-entities")
const htmlToText = require("html-to-text")

const { runWithDB } = require("./util")

const parseHtml = htmlString =>
  new Promise((resolve, reject) => {
    const parser = new htmlParser.Parser(
      new DomHandler((error, ast) => {
        if (error) reject(error)
        else resolve(ast)
      })
    )

    parser.write(htmlString)
    parser.end()
  })

const decodeEntities = text => new htmlEntities.AllHtmlEntities().decode(text)

const fetchSAndB = async () => {
  console.info(`${new Date()} -- Begin S&B fetch.`)

  const PUBLICATION_ID = "s-and-b"

  const fetchArticles = async (page, limit, attempts = 0) => {
    let response
    try {
      response = await fetch(
        `http://www.thesandb.com/?json=get_recent_posts&page=${page}&count=${limit}`
      )
    } catch (error) {
      console.error(error)
      const MAX_ATTEMPTS = 5
      if (attempts > MAX_ATTEMPTS) {
        throw new Error("Max fetch attempts made.  Exiting.")
      } else {
        console.error("Retrying fetch...")
        return await fetchArticles(page, limit, attempts + 1)
      }
    }

    if (!response.ok) {
      throw new Error(
        `Request failed with status ${response.status}: ${response.statusText}`
      )
    }

    const json = await response.json()

    return await Promise.all(
      json.posts.map(async post => {
        // Try to scrape the author out of the HTML

        const contentAst = await parseHtml(post.content)
        const AUTHOR_NODE_INDEX = 0
        const authorNode = contentAst[AUTHOR_NODE_INDEX]
        let authorName = null
        let authorEmail = null

        if (authorNode) {
          const authorLine = htmlToText
            .fromString(domUtils.getInnerHTML(authorNode), {
              wordwrap: false,
              ignoreHref: true,
              ignoreImage: true
            })
            .split(/\s+/)
            .filter(string => string.length > 0)

          const authorLineHasBold =
            authorNode.type === "tag" &&
            domUtils.existsOne(
              node => node.type === "tag" && node.name === "strong",
              authorNode.children
            )
          const authorLineHasBy = /[Bb]y/.test(authorLine[0])

          // Remove a leading "By "
          if (authorLineHasBy) {
            authorLine.splice(0, 1)
          }

          // Look for an email and splice it out if found
          const emailIndex = authorLine.findIndex(word =>
            /[\w\.]+@[\w\.]+/.test(word)
          )
          if (emailIndex >= 0) {
            authorEmail = authorLine
              .splice(emailIndex, 1)[0]
              .toLocaleLowerCase()
          }

          // Try to guess if the first line contains an author. If so, splice the
          // line out of the content
          if (
            authorLine.length > 1 &&
            authorLine.length < 5 &&
            (authorLineHasBold || authorLineHasBy)
          ) {
            authorName = authorLine.join(" ")
            contentAst.splice(AUTHOR_NODE_INDEX, 1)
          }
        }

        const authors = authorName
          ? [{ name: authorName, email: authorEmail }]
          : []

        const contentHtml = contentAst
          .map(node => domUtils.getOuterHTML(node))
          .join("")
        const content = htmlToText.fromString(contentHtml, {
          wordwrap: false,
          ignoreHref: true,
          ignoreImage: true
        })
        const wordCount = content.split(/\s+/).filter(s => s.length > 0).length
        const AVERAGE_WORDS_PER_MINUTE = 300
        const readTimeMinutes = Math.ceil(wordCount / AVERAGE_WORDS_PER_MINUTE)

        return {
          id: String(post.id),
          publication: PUBLICATION_ID,
          title: decodeEntities(post.title_plain).trim(),
          datePublished: new Date(post.date).valueOf(),
          dateEdited: new Date(post.modified).valueOf(),
          authors,
          headerImage:
            post.thumbnail_images && post.thumbnail_images.large
              ? post.thumbnail_images.large.url
              : null,
          content,
          readTimeMinutes
        }
      })
    )
  }

  try {
    await runWithDB(async db => {
      const articlesCollection = db.collection("articles")

      let numNewArticles = 0
      let numUpdatedArticles = 0

      const NUM_PAGES = 5
      const PAGE_SIZE = 400
      const pageNumbersToFetch = []
      for (let i = 0; i < NUM_PAGES; i++) {
        pageNumbersToFetch[i] = i + 1
      }

      console.info(`Scanning past ${NUM_PAGES * PAGE_SIZE} articles...`)

      await Promise.all(
        pageNumbersToFetch.map(async pageNumber => {
          const articlesFetched = await fetchArticles(pageNumber, PAGE_SIZE)

          await Promise.all(
            articlesFetched
              .map(async fetchedArticle => {
                const articleCursor = articlesCollection.find({
                  id: fetchedArticle.id,
                  publication: PUBLICATION_ID
                })
                if (await articleCursor.hasNext()) {
                  // Maybe update the article
                  const savedArticle = await articleCursor.next()
                  if (savedArticle.dateEdited !== fetchedArticle.dateEdited) {
                    const replaceResult = await articlesCollection.replaceOne(
                      { _id: savedArticle._id },
                      fetchedArticle
                    )

                    if (replaceResult.result.ok) numUpdatedArticles++
                    else console.error("Failed to replace article.")
                  }
                } else {
                  // Add the article
                  const insertResult = await articlesCollection.insertOne(
                    fetchedArticle
                  )

                  if (insertResult.result.ok) numNewArticles++
                  else console.error("Failed to insert article.")
                }
              })
              .map(promise => promise.catch(console.error))
          )
        })
      )

      console.info(
        `Success.  Found ${numNewArticles} new articles.  Updated ${numUpdatedArticles} articles.`
      )
    })
  } catch (error) {
    console.error(error)
  } finally {
    console.info(`${new Date()} -- End S&B fetch.\n`)
  }
}

schedule.scheduleJob(
  "fetch-s-and-b",
  { hour: 6, minute: 0 }, // Every day at 6:00 am
  fetchSAndB
)

fetchSAndB()
