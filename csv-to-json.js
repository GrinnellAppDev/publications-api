/**
 * @file csv-to-json.js
 *
 * Created by Zander Otavka on 5/7/17.
 * Copyright (C) 2016  Grinnell AppDev.
 *
 * A tool for creating batch write requests for DynamoDB tables when changing
 * out database schema.  Edit the transformItem function to correct the shape
 * of items.
 *
 * @license
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

const fs = require("fs")
const parse = require("csv-parse")

const inFilePath = process.argv[2]
const tableName = process.argv[3]
if (!inFilePath || !tableName) {
    console.error("Error: Arguments must be in the format: <infile> <table>")
}

/**
 * Modify each item to maintain compatibility if the database schema has changed.
 *
 * @example
 * const content = item.content.S
 * const wordCount = content.split(" ").length
 * item.readTimeMinutes = {N: String(wordCount / 450)}
 * return item
 *
 * @param {any} item the item to be added to the table with a put request.
 * @returns the modified item.
 */
function transformItem(item) {
    return item
}

let headerData
let firstRow = true
const requests = []

fs.createReadStream(inFilePath)
    .pipe(parse())
    .on("data", (data) => {
        if (firstRow) {
            headerData = data.map((header) => {
                const [, name, type] = /^(\w+) \((\w)\)$/.exec(header)
                return {name, type}
            })

            firstRow = false
        } else {
            let item = {}

            data.forEach((field, i) => {
                const {name, type} = headerData[i]

                if (!field) {
                    return
                }

                const JSON_TYPES = ["L", "M", "NS", "BS", "SS", "NULL", "BOOL"]
                if (JSON_TYPES.indexOf(type) !== -1) {
                    field = JSON.parse(field)
                }

                item[name] = {[type]: field}
            })

            item = transformItem(item)

            requests.push({
                PutRequest: {
                    Item: item,
                },
            })
        }
    })
    .on("finish", () => {
        fs.writeFileSync(tableName + ".json", JSON.stringify({
            [tableName]: requests,
        }, null, 4))
    })
