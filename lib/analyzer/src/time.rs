//! Designer : 東間日向
//! Date     : 2023/06/14
//! Purpose  : 時間情報を解析するパーサー群

use crate::{basic::*, digits::*};
use nom::{
    branch::alt,
    combinator::{map, map_opt},
    sequence::tuple,
    IResult,
};
use serde::Serialize;

/// 時間情報
#[derive(Debug, Serialize, PartialEq, Eq)]
pub struct Time {
    /// 時
    pub hour: Option<u8>,
    /// 分
    pub minute: Option<u8>,
}

impl Time {
    /// 新しい時間を生成する
    pub fn new(hour: Option<u8>, minute: Option<u8>) -> Self {
        Self { hour, minute }
    }

    /// 確定ていない項目があるかどうかを返す
    pub fn is_none(&self) -> bool {
        self.hour.is_none() && self.minute.is_none()
    }
}

/// 時の数値を解析するパーサー．時の範囲は0 ~ 23
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn hour(input: &str) -> IResult<&str, u8> {
    map_opt(digits, |hour| (hour <= 23).then(|| hour as u8))(input)
}

/// 分の数値を解析するパーサー．分の範囲は0 ~ 59
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn minute(input: &str) -> IResult<&str, u8> {
    map_opt(digits, |minute| (minute <= 59).then(|| minute as u8))(input)
}

/// 時間情報を解析するパーサー．
///
/// フォーマット
///
/// - <hour><colon><minute>
/// - <hour>時<minute>分
/// - <hour>時
///
/// * `input`  - 先頭に時間を含む文字列
///
/// 残りの文字列と解析した時間情報を返す
pub fn time_parser(input: &str) -> IResult<&str, Time> {
    alt((
        alt((
            // <hour><colon><minute>
            map(tuple((hour, colon, minute)), |(hour, _, minute)| {
                Time::new(Some(hour), Some(minute))
            }),
            // <hour>時<minute>分
            map(
                tuple((hour, char('時'), minute, char('分'))),
                |(hour, _, minute, _)| Time::new(Some(hour), Some(minute)),
            ),
            // <hour>時
            map(tuple((hour, char('時'))), |(hour, _)| {
                Time::new(Some(hour), Some(0))
            }),
        )),
        map(tag(""), |_| Time::new(None, None)),
    ))(input)
}

#[test]
fn test_time_parser() {
    assert_eq!(time_parser("03:03"), Ok(("", Time::new(Some(3), Some(3)))));
    assert_eq!(
        time_parser("六時五十五分"),
        Ok(("", Time::new(Some(6), Some(55))))
    );
    assert_eq!(time_parser("０時"), Ok(("", Time::new(Some(0), Some(0)))));
}
