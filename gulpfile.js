'use strict';

var argv = require('yargs').argv;

// =======================================================================
// Gulp Plugins
// =======================================================================
var gulp = require('gulp'),
    connect = require('gulp-connect'),
    jshint = require('gulp-jshint'),
    stylish = require('jshint-stylish'),
    jscs = require('gulp-jscs'),
    concat = require('gulp-concat'),
    streamify = require('gulp-streamify'),
    uglify = require('gulp-uglify'),
    sourcemaps = require('gulp-sourcemaps'),
    less = require('gulp-less'),
    prefix = require('gulp-autoprefixer'),
    minifyCSS = require('gulp-minify-css'),
    notify = require('gulp-notify'),
    browserify = require('browserify'),
    watchify = require('watchify'),
    del = require('del'),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    runSequence = require('run-sequence'),
    karma = require('karma').server,
    gulpif = require('gulp-if');


// =======================================================================
// File Paths
// =======================================================================
var filePath = {
    build: {
        dest: './static'
    },
    lint: {
        src: ['./js/app/*.js', './js/app/**/*.js']
    },
    browserify: {
        src: './js/app/app.js',
        watch: [
            '!./js/app/assets/libs/*.js',
            '!./js/app/assets/libs/**/*.js',
            '!./js/app/**/*.spec.js',
            './js/app/*.js', './js/app/**/*.js',
            './js/app/**/*.html'
        ]
    },
    styles: {
        src: './js/app/app.less',
        watch: ['./js/app/app.less', './js/app/**/*.less']
    },
    assets: {
        images: {
            src: './js/app/assets/images/**/*',
            watch: ['./js/app/assets/images', './js/app/assets/images/**/*'],
            dest: './static/images/'
        },
        fonts: {
            src: ['./js/libs/font-awesome/fonts/*'],
            dest: './static/fonts/'
        }
    },
    vendorJS: {
        // These files will be bundled into a single vendor.js file that's called at the bottom of index.html
        src: [
            './js/libs/angular/angular.js',
            './js/libs/angular-animate/angular-animate.js',
            './js/libs/angular-bootstrap/ui-bootstrap-tpls.js',
            './js/libs/angular-cookies/angular-cookies.js',
            './js/libs/angular-resource/angular-resource.js',
            './js/libs/angular-sanitize/angular-sanitize.js',
            './js/libs/angular-ui-router/release/angular-ui-router.js',
            './js/libs/jquery/dist/jquery.js',
            './js/libs/bootstrap/dist/js/bootstrap.js',
            './js/libs/domready/ready.js',
            './js/libs/lodash/lodash.js',
            './js/libs/restangular/dist/restangular.js'
        ]
    },
    //vendorCSS: {
    //    src: [
    //        './libs/bootstrap/dist/css/bootstrap.css', // v3.1.1
    //        './libs/font-awesome/css/font-awesome.css' // v4.1.0
    //    ]
    //},
    copyIndex: {
        src: './js/app/index.html',
        watch: './js/app/index.html'
    },
    copyFavicon: {
        src: './js/app/favicon.png'
    }
};


// =======================================================================
// Error Handling
// =======================================================================
function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}


// =======================================================================
// Server Task
// =======================================================================
var express = require('express'),
    server = express();
// Server settings
server.use(express.static(filePath.build.dest));
// Redirects everything back to our index.html
server.all('/*', function(req, res) {
    res.sendfile('/', {
        root: filePath.build.dest
    });
});
// uncomment the "middleware" section when you are ready to connect to an API
gulp.task('server', function() {
    connect.server({
        root: filePath.build.dest,
        fallback: filePath.build.dest + '/index.html',
        port: 5000,
        livereload: true
        // ,
        // middleware: function(connect, o) {
        //     return [ (function() {
        //         var url = require('url');
        //         var proxy = require('proxy-middleware');
        //         var options = url.parse('http://localhost:3000/'); // path to your dev API
        //         options.route = '/api';
        //         return proxy(options);
        //     })() ];
        // }
    });
});


// =======================================================================
// Clean out dist folder contents on build
// =======================================================================
gulp.task('clean-dev', function() {
    del(['./static/*.js',
        './static/*.css',
        '!./static/vendor.js',
        '!./static/vendor.css',
        './static/*.html',
        './static/*.png',
        './static/*.ico',
        './reports/**/*',
        './reports']);
});

gulp.task('clean-full', function() {
    del(['./static/*',
        './reports/**/*',
        './reports']);
});


// =======================================================================
// JSHint
// =======================================================================
gulp.task('lint', function() {
    return gulp.src(filePath.lint.src)
    .pipe(jshint())
    .pipe(jshint.reporter(stylish));
});


// =======================================================================
// Javascript Checkstyles (JSCS)
// =======================================================================
gulp.task('checkstyle', function() {
    return gulp.src(filePath.lint.src)
    .pipe(jscs())
    .on('error', handleError);
});


// =======================================================================
// Browserify Bundle
// =======================================================================

var bundle = {};
bundle.conf = {
    entries: filePath.browserify.src,
    external: filePath.vendorJS.src,
    debug: true,
    cache: {},
    packageCache: {}
};

function rebundle() {
    return bundle.bundler.bundle()
        .pipe(source('bundle.js'))
        .on('error', handleError)
        .pipe(buffer())
        .pipe(gulpif(!bundle.prod, sourcemaps.init({
            loadMaps: true
        })))
        .pipe(gulpif(!bundle.prod, sourcemaps.write('./')))
        .pipe(gulpif(bundle.prod, streamify(uglify({
            mangle: false
        }))))
        .pipe(gulp.dest(filePath.build.dest))
        .pipe(connect.reload());
}

function configureBundle(prod) {
    bundle.bundler = watchify(browserify(bundle.conf));
    bundle.bundler.on('update', rebundle);
    bundle.prod = prod;
}

gulp.task('bundle-dev', function () {
    'use strict';
    configureBundle(false);
    return rebundle();
});

gulp.task('bundle-prod', function () {
    'use strict';
    configureBundle(true);
    return rebundle();
});


// =======================================================================
// Styles Task
// =======================================================================
gulp.task('styles-dev', function() {
    return gulp.src(filePath.styles.src)
    .pipe(sourcemaps.init())
    .pipe(less())
    .on('error', handleError)
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(filePath.build.dest))
    .on('error', handleError)
    .pipe(notify({
        message: 'Styles task complete'
    }))
    .pipe(connect.reload());
});

gulp.task('styles-prod', function() {
    return gulp.src(filePath.styles.src)
    .pipe(less())
    .on('error', handleError)
    .pipe(prefix('last 1 version', '> 1%', 'ie 8', 'ie 7', {
        map: true
    }))
    .pipe(minifyCSS())
    .pipe(gulp.dest(filePath.build.dest))
    .on('error', handleError)
    .pipe(notify({
        message: 'Styles task complete'
    }));
});


// =======================================================================
// Images Task
// =======================================================================
gulp.task('images', function() {
    return gulp.src(filePath.assets.images.src)
    .on('error', handleError)
    .pipe(gulp.dest(filePath.assets.images.dest))
    .pipe(notify({
        message: 'Images copied'
    }))
    .pipe(connect.reload());
});


// =======================================================================
// Fonts Task
// =======================================================================
gulp.task('fonts', function () {
    return gulp.src(filePath.assets.fonts.src)
        .on('error', handleError)
        .pipe(gulp.dest(filePath.assets.fonts.dest))
        .pipe(connect.reload());
});


// =======================================================================
// Vendor JS Task
// =======================================================================
gulp.task('vendorJS', function() {
    var b = browserify({
        debug: true,
        require: filePath.vendorJS.src
    });

    return b.bundle()
    .pipe(source('vendor.js'))
    .on('error', handleError)
    .pipe(buffer())
    .pipe(uglify())
    .pipe(gulp.dest(filePath.build.dest))
    .pipe(notify({
        message: 'VendorJS task complete'
    }));
});


// =======================================================================
// Vendor CSS Task
// =======================================================================
//gulp.task('vendorCSS', function() {
//    return gulp.src(filePath.vendorCSS.src)
//    .pipe(concat('vendor.css'))
//    .on('error', handleError)
//    .pipe(minifyCSS())
//    .pipe(gulp.dest(filePath.build.dest))
//    .pipe(notify({
//        message: 'VendorCSS task complete'
//    }))
//    .pipe(connect.reload());
//});


// =======================================================================
// Copy index.html
// =======================================================================
gulp.task('copyIndex', function() {
    return gulp.src(filePath.copyIndex.src)
    .pipe(gulp.dest(filePath.build.dest))
    .pipe(notify({
        message: 'index.html successfully copied'
    }))
    .pipe(connect.reload());
});


// =======================================================================
// Copy Favicon
// =======================================================================
gulp.task('copyFavicon', function() {
    return gulp.src(filePath.copyFavicon.src)
    .pipe(gulp.dest(filePath.build.dest))
    .pipe(notify({
        message: 'favicon successfully copied'
    }));
});


// =======================================================================
// Watch for changes
// =======================================================================
gulp.task('watch', function() {
    gulp.watch(filePath.styles.watch, ['styles-dev']);
    gulp.watch(filePath.assets.images.watch, ['images']);
    gulp.watch(filePath.vendorJS.src, ['vendorJS']);
    gulp.watch(filePath.copyIndex.watch, ['copyIndex']);
    gulp.watch(filePath.lint.src, ['checkstyle']);
    console.log('Watching...');
});


// =======================================================================
// Karma Configuration
// =======================================================================
gulp.task('karma', function(done) {
    karma.start({
        configFile: __dirname + '/karma.conf.js',
        singleRun: !argv.watch
    }, done);
});


// =======================================================================
// Sequential Build Rendering
// =======================================================================

// run "gulp" in terminal to build the DEV app
gulp.task('build-dev', function(callback) {
    runSequence(
        ['clean-dev', 'lint', 'checkstyle'],
        // images and vendor tasks are removed to speed up build time. Use "gulp build" to do a full re-build of the dev app.
        ['bundle-dev', 'styles-dev', 'copyIndex', 'copyFavicon'], ['server', 'watch'],
        callback
    );
});

// run "gulp test" in terminal to build the DEV app
gulp.task('build-test', function(callback) {
    runSequence(
        ['clean-full', 'lint', 'checkstyle'],
        ['karma'],
        callback
    );
});

// run "gulp prod" in terminal to build the PROD-ready app
gulp.task('build-prod', function(callback) {
    runSequence(
        ['clean-full', 'lint', 'checkstyle'],
        ['bundle-prod', 'styles-prod', 'images', 'fonts', 'vendorJS', 'copyIndex', 'copyFavicon'],
        ['server'],
        callback
    );
});

// run "gulp build" in terminal for a full re-build in DEV
gulp.task('build', function(callback) {
    runSequence(
        ['clean-full', 'lint', 'checkstyle'],
        ['bundle-dev', 'styles-dev', 'images', 'fonts', 'vendorJS', 'copyIndex', 'copyFavicon'],
        ['server', 'watch'],
        callback
    );
});

gulp.task('default', ['build-dev']);
gulp.task('test', ['build-test']);
gulp.task('prod', ['build-prod']);
