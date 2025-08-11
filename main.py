import dash
from dash import Dash, html, clientside_callback, Input, Output
from flask import Flask
from pages import opcua, home, about

index_str = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-LCWNJQRXQH"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-LCWNJQRXQH');
        </script>
        <!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "0ded497d3a654a6daab165aabc396559"}'></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app = Flask(__name__, instance_relative_config=True)
dash_app = Dash(__name__,
        server=app,
        use_pages=True,
        assets_folder='static',
        index_string=index_str,
        external_scripts=[{
            'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js',
            'integrity': 'sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm',
            'crossorigin': 'anonymous'
        }],
        external_stylesheets=[{
            'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css',
            'integrity': 'sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9',
            'crossorigin': 'anonymous',
            'rel': 'stylesheet'
        },
        {
            'href': 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
            'rel': 'stylesheet'
        }]
    )

# Register pages
dash.register_page('pages.homepage',
    path='/',
    title='SARS-CoV-2 Overview',
    name='SARS-CoV-2 Overview',
    layout=home.layout)
dash.register_page('pages.opcua',
    path='/opcua',
    title='Configurations',
    name='Configurations',
    layout=opcua.layout)
dash.register_page('pages.about',
    path='/about',
    title='About',
    name='About',
    layout=about.layout)

# Add clientside callback for sidebar toggle
clientside_callback(
    """
    function(n_clicks) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('active');
            
            // Adjust content margin when sidebar is toggled
            const content = document.querySelector('.content');
            if (content) {
                if (sidebar.classList.contains('active')) {
                    content.style.marginLeft = '270px';
                } else {
                    content.style.marginLeft = '0';
                }
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('sidebarCollapse', 'data-dummy'),  # Dummy output
    Input('sidebarCollapse', 'n_clicks'),
)

with app.app_context():
    dash_app.layout = dash.page_container

if __name__ == "__main__":
    app.run(debug=True, port=8052)