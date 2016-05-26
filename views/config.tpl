<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>{{name}}</title>
</head>
<body>
    <h1>{{name}}</h1>
    <textarea id="test_text">Try me!</textarea>
    <div id="result"></div>
    <button onclick="test_ws();">Try</button>
    <h3>Raw configuration</h3>
    <pre>{{config}}</pre>
    <script>
        function test_ws () {
            var text = document.getElementById('test_text').value;
            var req = new XMLHttpRequest();
            function update () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    console.log(this.responseText);
                    res = JSON.parse(this.responseText).result;
                    document.getElementById('result').textContent = res;
                }
            }
            req.onreadystatechange = update;
            req.open("POST", "/run/{{name}}");
            req.setRequestHeader('Content-Type','application/json');
            req.send(JSON.stringify({text:text}));
        }
    </script>
</body>
</html>
