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
  console.info(`${new Date()} -- Fetching from S&B`)

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

    const json = await response.json()

    return await Promise.all(
      json.posts.map(async post => {
        const contentAst = await parseHtml(post.content)
        const authorP = contentAst[0]
        let authorName = null
        let authorEmail = null
        if (authorP.type === "tag" && authorP.name === "p") {
          const authorNameWrapper = authorP.children.find(
            node => node.type === "tag" && node.name === "strong"
          )
          if (authorNameWrapper) {
            authorName = authorNameWrapper.children
              .filter(node => node.type === "text")
              .map(node => node.data.trim())
              .join(" ")
              .trim()
              .replace(/^By /, "")

            if (authorName) {
              const emailWrapper = authorP.children.find(
                node => node.type === "text"
              )
              if (emailWrapper) {
                authorEmail = decodeEntities(emailWrapper.data).trim() || null
              }

              contentAst.splice(0, 1)
            }
          }
        }

        const contentHtml = contentAst
          .map(node => domUtils.getOuterHTML(node))
          .join("")
        const content = htmlToText.fromString(contentHtml, {
          wordwrap: false,
          ignoreHref: true,
          ignoreImage: true
        })
        const wordCount = content.split(/\s+/).filter(s => s.length > 0).length
        // Average college student reading speed in words per minute
        const AVERAGE_WPM = 300
        const readTimeMinutes = Math.ceil(wordCount / AVERAGE_WPM)

        return {
          id: post.id,
          publication: PUBLICATION_ID,
          title: decodeEntities(post.title_plain).trim(),
          datePublished: new Date(post.date).valueOf(),
          dateEdited: new Date(post.modified).valueOf(),
          authors: authorName ? [{ name: authorName, email: authorEmail }] : [],
          headerImage: post.thumbnail_images
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
      const removeKnownArticles = async ([article, ...otherArticles]) => {
        if (!article) {
          return []
        } else if (
          await articlesCollection.find({ id: article.id }).hasNext()
        ) {
          // Article is already in the database
          return removeKnownArticles(otherArticles)
        } else {
          // Article is new
          return [article, ...removeKnownArticles(otherArticle)]
        }
      }
      const fetchUnknown = async (startPage = 0) => {
        const PAGE_SIZE = 10
        const newArticles = await removeKnownArticles(
          await fetchArticles(startPage, PAGE_SIZE)
        )

        // Keep fetching until page 20 or a page contains no new articles
        const MAX_PAGES = 20
        if (newArticles.length > 0 && startPage < MAX_PAGES) {
          return [...newArticles, ...fetchUnknown(startPage + 1)]
        } else {
          return newArticles
        }
      }

      const MAX_INITIAL_LOAD = 100
      const articles =
        (await articlesCollection.count({ publication: PUBLICATION_ID })) > 0
          ? await fetchUnknown()
          : await fetchArticles(0, MAX_INITIAL_LOAD)

      if (articles.length > 0) {
        const insertResult = await articlesCollection.insertMany(articles)
        if (!insertResult.result.ok) {
          throw new Error("Database insert failed")
        } else {
          console.info(`Downloaded ${insertResult.insertedCount} articles`)
        }
      } else {
        console.info("No new articles")
      }
    })
  } catch (error) {
    console.error(error)
  } finally {
    console.info(`${new Date()} -- end S&B fetch\n`)
  }
}

fetchSAndB()

if (process.env.NODE_ENV === "production") {
  schedule.scheduleJob(
    "fetch-s-and-b",
    { dayOfWeek: 5, hour: 6, minute: 0 }, // Every Friday at 6:00 am
    fetchSAndB
  )
}
