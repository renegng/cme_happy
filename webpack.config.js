const autoprefixer = require('autoprefixer');

module.exports = {
    entry: [
        './instance/js/swing_firebase-api-init.js',
        './static/css/swing_app.scss',
        './static/js/swing_firebase.js',
        './static/js/lazysizes.min.js',
        './static/js/swing_app.js'
    ],
    output: {
        path: __dirname,
        filename: 'static/js/swing-bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    { loader: 'file-loader',
                        options: {
                            name: 'static/css/swing-bundle.css',
                        },
                    },
                    { loader: 'extract-loader' },
                    { loader: 'css-loader' },
                    { loader: 'postcss-loader',
                        options: {
                            plugins: () => [autoprefixer()]
                        },
                    },
                    { loader: 'sass-loader',
                        options: {
                            // Prefer Dart Sass
                            implementation: require('sass'),
                            sassOptions: {
                                includePaths: ['./node_modules'],
                            },
                            webpackImporter: false,
                        },
                    }
                ],
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                query: {
                    presets: [
                        [
                            '@babel/preset-env', {
                                'useBuiltIns': 'entry',
                                'corejs': {'version': '3', 'proposals': true},
                            }
                        ]
                    ],
                },
            }
        ],
    },
};