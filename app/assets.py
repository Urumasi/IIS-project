from flask_assets import Bundle, Environment

js = Bundle(
    'js/test.js',
    filters='jsmin',
    output='gen/packed.js'
)

css = Bundle(
    'css/style.css',
    filters='cssmin',
    output='gen/packed.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
