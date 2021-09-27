
const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    // const sass = require("gulp-sass");
    var sass = require('gulp-sass')(require('sass'));
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");
    return gulp
    .src("assets/scss/styles.scss")    // .scss 파일 찾기
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([                    // .scss 에 있는 코드들(@tailwindcss 등)을 css로 바꿈
        require("tailwindcss"),
        require("autoprefixer")]))
    .pipe(minify())                    // 파일 사이즈를 줄임
    .pipe(gulp.dest("static/css"));    // pipe의 결과물을 static/css로 보냄
};

exports.default = css;