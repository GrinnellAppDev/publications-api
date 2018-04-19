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
      if (attempts > 5) {
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
              authorEmail =
                decodeEntities(
                  authorP.children.find(node => node.type === "text").data
                ).trim() || null

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
          // TODO: calculate from plaintext content
          readTimeMinutes: 0
        }
      })
    )
  }

  try {
    await runWithDB(async db => {
      const articlesCollection = db.collection("articles")
      let articles
      if (
        (await articlesCollection.count({ publication: PUBLICATION_ID })) > 0
      ) {
        const fetchUnknown = async (startPage = 0) => {
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

          const articles = await removeKnownArticles(
            await fetchArticles(startPage, 10)
          )

          if (articles.length > 0) {
            return [...articles, ...fetchUnknown(startPage + 1)]
          } else {
            return articles
          }
        }

        articles = await fetchUnknown()
      } else {
        articles = await fetchArticles(0, 10)
      }

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
