import { sort } from 'd3';

const d3 = require('d3');

const Visualisation = {
    init: () => {
        let sortData;
        d3.json("https://raw.githubusercontent.com/sinanatra/weekly-album-genre/master/data.json")
            .then(function (data) {
                const dataKeys = Object.keys(data)

                let newData = []
                dataKeys.forEach(element => {
                    let line = data[element]
                    let newJson = {
                        genre: element,
                        albums: line
                    }
                    newData.push(newJson)
                });

                sortData = newData.sort(function (a, b) { return b.albums.length - a.albums.length });
                console.log(sortData);

                const svg = d3.select("#visualisation")

                svg.selectAll("div")
                    .data(sortData)
                    .enter()
                    .append("div")
                    .text((d) => d.genre)
                    .attr('class', 'words')
                    .attr('attr', (d) => d.genre)
                    .style('width', (d) => d3.randomUniform(99)() + '%')
                    .style('text-align', 'right')
                    .style('background', (d) => randomColor())
                    .on("click", function (d) {
                        var active = d.path[0].active ? true : false,
                            newOpacity = active ? 0 : 1;
                        d3.select(".links").style("opacity", newOpacity);
                        d.path[0].active = active;
                        addElement(d.path[0])
                    })


                function addElement(elem) {
                    d3.selectAll('.links').remove()
                    d3.select(elem)
                        .append('div')
                        .attr('class', 'links')
                        .html(function (d) {
                            let albums = ''
                            d.albums.forEach(element => {
                                // albums += '<a class="iframes" target="_blank" href=' + element + '>' + 'Listen' + '</a>'
                                albums += "<iframe src=https://open.spotify.com/embed/album/" + element + " width='300' height='80' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe>"
                            });
                            return albums
                        })
                }
            })

        let toggled = 'false'
        d3.select(".sort")
            .on("click", function (d) {
                if (toggled == 'false') {
                    toggled = 'true'
                    d3.selectAll('.words')
                        .style('width', function (d) {
                            let percentage = Math.round(d.albums.length * 99 / sortData[0].albums.length) + "%";
                            return percentage ;
                        })
                }
                else {
                    toggled = 'false'
                    d3.selectAll('.words')
                        .style('width', function (d) {
                            return d3.randomUniform(80)() + '%';
                        })
                }
            })
    }
};

export default Visualisation;


var randomColor = (function () {
    var golden_ratio_conjugate = .98;
    var h = Math.random();

    var hslToRgb = function (h, s, l) {
        var r, g, b;

        if (s == 0) {
            r = g = b = l; // achromatic
        } else {
            function hue2rgb(p, q, t) {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1 / 6) return p + (q - p) * 6 * t;
                if (t < 1 / 2) return q;
                if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
                return p;
            }

            var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            var p = 2 * l - q;
            r = hue2rgb(p, q, h + 1 / 3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1 / 3);
        }

        return '#' + Math.round(r * 255).toString(16) + Math.round(g * 255).toString(16) + Math.round(b * 255).toString(16);
    };

    return function () {
        h += golden_ratio_conjugate;
        h %= 1;
        return hslToRgb(h, 0.5, 0.60);
    };
})();