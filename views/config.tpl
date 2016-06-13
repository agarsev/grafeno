<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Grafeno: {{name}}</title>
    <meta name="description" content="Example API page for Grafeno by Antonio F. G. Sevilla" />
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            background: #E8EDEF;
            color: #426A7B;
            padding: 5vw;
        }
        #loading {
            display: inline-block;
            margin-left: 1em;
            height: 16px;
            width: 16px;
            background: url('data:image/gif;base64,R0lGODlhEAAQAPIAAOjt70Jqe8DO02yLmUJqe4Gcp5astqG1vSH+GkNyZWF0ZWQgd2l0aCBhamF4bG9hZC5pbmZvACH5BAAKAAAAIf8LTkVUU0NBUEUyLjADAQAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQACgABACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkEAAoAAgAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkEAAoAAwAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkEAAoABAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQACgAFACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQACgAGACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAAKAAcALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==');
        }
        .hidden {
            visibility: hidden;
        }
        div {
            display: inline-block;
            overflow: auto;
        }
        h1,h3 {
            color: black;
        }
        a {
            color: #45856B;
        }
        pre {
            display: inline-block;
            border: 1px solid #426A7B;
            background: white;
            padding: 2ex;
        }
        textarea {
            width: 35vw;
        }
        #result {
            float: right;
            border: 1px solid #426A7B;
            background: white;
            width: 45vw;
            height: 50vw;
        }
        .graphdisplay {
            overflow: hidden !important;
        }
    </style>
</head>
<body>
    <h1>Service: {{name}}</h1>
    <div>
        <textarea rows="5" id="test_text">{{default_text}}</textarea>
        <p><button id="send_button" onclick="test_ws();">Send</button><span id="loading" class="hidden"></span></p>
    </div>
    <div id="result"></div>
    <div>
        <h3>Raw configuration</h3>
        <pre>{{config}}</pre>
    </div>
    <div>
        <h3>Credits</h3>
        <ul>
        <li>Code &mdash;coming soon</li>
        <li><a href="http://visjs.org/">vis.js</a></li>
        <li><a href="http://nlp.lsi.upc.edu/freeling/node/1">FreeLing</a></li>
        <li>By <a href="https://garciasevilla.com">Antonio F. G. Sevilla</a> <a href="mailto:afgs@ucm.es">&lt;afgs@ucm.es&gt;</a></li>
        <li>Part of <a href="http://nil.fdi.ucm.es/">NiL &mdash;Natural Interaction based on language</a></li>
        <li>Financed by <a href="http://conceptcreationtechnology.eu/">ConCreTe &mdash;Concept Creation Technology</a></li>
        </ul>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"></script>
    <script>
        var resdiv = document.getElementById('result');
        var test_text = document.getElementById('test_text');
        var send_button = document.getElementById('send_button');
        var loading = document.getElementById('loading');

        function update () {
            if (this.readyState === XMLHttpRequest.DONE) {
                console.log(this.responseText);
                var res = JSON.parse(this.responseText);
                if (res.ok) {
                    res = res.result;
                    if (typeof res === 'object') {
                        var nodes = new vis.DataSet(res.nodes);
                        res.links.forEach(function (e) {
                            e.from = res.nodes[e.source].id;
                            e.to = res.nodes[e.target].id;
                        });
                        var edges = new vis.DataSet(res.links);
                        var network = new vis.Network(resdiv, {nodes:nodes,edges:edges}, {edges:{arrows:"to"}});
                        resdiv.className = 'graphdisplay';
                    } else {
                        resdiv.textContent = res;
                        resdiv.className = '';
                    }
                } else {
                    resdiv.textContent = "There was an error: "+res.error_message;
                    resdiv.className = '';
                }
                send_button.disabled = false;
                loading.className = 'hidden';
            }
        }

        function test_ws () {
            loading.className = '';
            send_button.disabled = true;
            var req = new XMLHttpRequest();
            req.onreadystatechange = update.bind(req);
            req.open("POST", "/run/{{name}}");
            req.setRequestHeader('Content-Type','application/json');
            req.send(JSON.stringify({text:test_text.value}));
        }
    </script>
</body>
</html>
