from flask_assets import Bundle, Environment

js = Bundle(
    filters='jsmin',
    output='gen/packed.js'
)

js_term = Bundle(
    'js/bespoke/term_details.js',
    filters='jsmin',
    output='gen/term_detail.js'
)

css = Bundle(
    'css/style.css',
    filters='cssmin',
    output='gen/packed.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
assets.register('js_term', js_term)
