//! Designer    : 東間日向
//! Date        : 2023/06/14
//! Purpose     : 日付情報の定義とその解析

use crate::{basic::*, digits::*};
use nom::{
    branch::alt,
    combinator::{map, map_opt},
    sequence::tuple,
    IResult,
};
use serde::Serialize;

#[derive(Debug, Serialize, PartialEq, Eq)]
/// 日付情報
pub struct Date {
    /// 年
    pub year: Option<u16>,
    /// 月
    pub month: Option<u8>,
    /// 日
    pub day: Option<u8>,
}

impl Date {
    /// 新しい日付を生成する
    pub fn new(year: Option<u16>, month: Option<u8>, day: Option<u8>) -> Self {
        Self { year, month, day }
    }

    /// 確定ていない項目があるかどうかを返す
    pub fn is_none(&self) -> bool {
        self.year.is_none() && self.month.is_none() && self.day.is_none()
    }
}

/// 年の数値を解析するパーサー．年の範囲は1 ~ 9999
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn year(input: &str) -> IResult<&str, u16> {
    map_opt(digits, |year| {
        (1 <= year && year <= 9999).then(|| year as u16)
    })(input)
}

/// 月の数値を解析するパーサー．月の範囲は1 ~ 12
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn month(input: &str) -> IResult<&str, u8> {
    map_opt(digits, |month| {
        (1 <= month && month <= 12).then(|| month as u8)
    })(input)
}

/// 日の数値を解析するパーサー．日の範囲は1 ~ 31
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn day(input: &str) -> IResult<&str, u8> {
    map_opt(digits, |day| (1 <= day && day <= 31).then(|| day as u8))(input)
}

/// 日付を取得する
///
/// * `offset`  - 取得する日付のオフセット
///
/// 現在の日付から`offset`日後の日付を返す
fn get_day(offset: u8) -> Date {
    use chrono::prelude::{Datelike, FixedOffset, Utc};
    use chrono::Duration;
    let dt = Utc::now().with_timezone(&FixedOffset::east_opt(9 * 3600).unwrap());
    let dt = dt + Duration::days(offset as i64);
    Date::new(
        Some(dt.year() as u16),
        Some(dt.month() as u8),
        Some(dt.day() as u8),
    )
}

/// 日付情報を解析するパーサー．
///
/// フォーマット
///
/// - 今日
/// - 明日
/// - 明後日
/// - <month><slash><day>
/// - <year><slash><month><slash><day>
/// - <month>月<day>日
/// - <year>年<month>月<day>日
///
/// * `input`  - 先頭に日付を含む文字列
///
/// 残りの文字列と解析した日付情報を返す
pub fn date_parser(input: &str) -> IResult<&str, Date> {
    alt((
        // 今日
        map(tag("今日"), |_| get_day(0)),
        // 明日
        map(tag("明日"), |_| get_day(1)),
        // 明後日
        map(tag("明後日"), |_| get_day(2)),
        // 明々後日
        map(tag("明々後日"), |_| get_day(3)),
        // <year><slash><month><slash><day>
        map(
            tuple((year, slash, month, slash, day)),
            |(year, _, month, _, day)| Date::new(Some(year), Some(month), Some(day)),
        ),
        // <month><slash><day>
        map(tuple((month, slash, day)), |(month, _, day)| {
            Date::new(None, Some(month), Some(day))
        }),
        // <month>月<day>日
        map(
            tuple((month, char('月'), day, char('日'))),
            |(month, _, day, _)| Date::new(None, Some(month), Some(day)),
        ),
        // <year>年<month>月<day>日
        map(
            tuple((year, char('年'), month, char('月'), day, char('日'))),
            |(year, _, month, _, day, _)| Date::new(Some(year), Some(month), Some(day)),
        ),
    ))(input)
}

#[test]
fn test_date_parser() {
    assert_eq!(
        date_parser("2/15"),
        Ok(("", Date::new(None, Some(2), Some(15))))
    );
    assert_eq!(
        date_parser("2023/2/15"),
        Ok(("", Date::new(Some(2023), Some(2), Some(15))))
    );
    assert_eq!(
        map(
            tuple((year, slash, month, slash, day)),
            |(year, _, month, _, day)| { Date::new(Some(year), Some(month), Some(day)) }
        )("2023/7/11 16:30"),
        Ok((" 16:30", Date::new(Some(2023), Some(7), Some(11))))
    );
}
