<html>
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
        <script>
            function subst() {
            var vars={};
            var x=document.location.search.substring(1).split('&');
            for(var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
            var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
            for(var i in x) {
            var y = document.getElementsByClassName(x[i]);
            for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
                }
            }
        </script>
    </head>
    <body style="border:0; margin: 0;" onload="subst()">
        <table style="border-top: 1px solid black; width: 100%">
            <tr >
                <td style="text-align:right;font-size:12;" width="95%">Page <span class="page"/></td><td style="text-align:left;font-size:12;">  of <span class="topage"/></td>
            </tr>
        </table>
    </body>
</html>