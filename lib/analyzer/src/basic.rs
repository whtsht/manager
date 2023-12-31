//! Designer    : 東間日向
//! Date        : 2023/06/13
//! Purpose     : 空白やコロンなど基本的なパーサープログラム

use nom::{
    branch::alt,
    bytes::complete::take_while,
    combinator::map,
    sequence::{preceded, terminated},
    IResult,
};

/// 空白文字を読み飛ばすパーサー
///
/// * `input`     - 入力文字列
///
/// 手前の空白が読み飛ばさせた残りの文字列
pub fn spaces(input: &str) -> IResult<&str, ()> {
    map(take_while(move |c| " 　\t\n".contains(c)), |_| ())(input)
}

/// 指定された文字を読むパーサーを返す
///
/// * `target`     - 読み飛ばしたい文字
///
/// `target`を読み飛ばすパーサー
pub fn char<'a>(target: char) -> impl FnMut(&'a str) -> IResult<&'a str, char> {
    preceded(
        spaces,
        terminated(nom::character::complete::char(target), spaces),
    )
}

/// 指定された文字列を読むパーサーを返す
///
/// * `target`     - 読み飛ばしたい文字列
///
/// `target`を読み飛ばすパーサー
pub fn tag<'a>(target: &'a str) -> impl FnMut(&'a str) -> IResult<&'a str, &'a str> {
    preceded(
        spaces,
        terminated(nom::bytes::complete::tag(target), spaces),
    )
}

/// 指定された文字列内のいずれかの文字を読むパーサーを返す
///
/// * `target`     - 読み飛ばしたい文字を含む文字列
///
/// `target`のいずれか1文字を読み飛ばすパーサー
pub fn one_of<'a>(target: &'a str) -> impl FnMut(&'a str) -> IResult<&'a str, char> {
    nom::character::complete::one_of(target)
}

/// スラッシュを読み飛ばすパーサー
pub fn slash(input: &str) -> IResult<&str, char> {
    alt((char('/'), char('／')))(input)
}

/// コロンを読み飛ばすパーサー
pub fn colon(input: &str) -> IResult<&str, char> {
    alt((char(':'), char('：')))(input)
}
