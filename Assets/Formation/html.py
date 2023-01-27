def designHeader(title: str) -> str:
    header = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta ' \
             f'http-equiv="X-UA-Compatible" content="IE=edge">\n\t<meta name="viewport" content="width=device-width, ' \
             f'initial-scale=1.0">\n\t<link ' \
             f'rel="stylesheet" href="css/style.css">\n\t<title>' \
             f'{title}</title>\n</head> '
    return header


def designFooter() -> str:
    footer = """
<footer class="footer">
    <div class="container">
        <div>
            <h1>Loruki</h1>
            <p>Copyright &copy; 2020</p>
        </div>
        <nav>
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="features.html">features</a></li>
                <li><a href="docs.html">Docs</a></li>
            </ul>
        </nav>
        <div class="social">
            <a href="#"><i class="fab fa-github fa2x"></i></a>
            <a href="#"><i class="fab fa-facebook fa2x"></i></a>
            <a href="#"><i class="fab fa-instagram fa2x"></i></a>
            <a href="#"><i class="fab fa-twitter fa2x"></i></a>
        </div>
    </div>

</footer>
</body>
</html>
    """
    return footer
