//! Designer    : 東間日向
//! Date        : 2023/06/14
//! Purpose     : 時刻情報の定義とその解析

use crate::{date::*, time::*};
use nom::{branch::alt, combinator::map, sequence::tuple, IResult};
use once_cell::sync::Lazy;
use serde::Serialize;

#[derive(Debug, Serialize, PartialEq, Eq)]
/// 時刻情報
pub struct DateTime {
    /// 日付情報
    pub date: Date,
    /// 時間情報
    pub time: Time,
}

impl DateTime {
    /// 新しい時刻を生成する
    fn new(date: Date, time: Time) -> Self {
        Self { date, time }
    }
}

/// csv形式の文字列をVecに変換する
///
/// * `s`   : csv形式の文字列
///
/// 変換したVec
fn csv_to_vec(s: &str) -> Vec<&str> {
    s.split(|c| c == ',' || c == ' ' || c == '\n').collect()
}

/// 「明日」「日」などの時刻を表す文字の集合を表す．
pub fn time_word() -> &'static Vec<&'static str> {
    static WORD: Lazy<Vec<&str>> = Lazy::new(|| {
        let csv = include_str!("../time_word.csv");
        csv_to_vec(csv).into_iter().filter(|&s| s != "").collect()
    });
    &WORD
}

/// 文字列を受け取り，時刻に関係ない文字をフィルタリングする．
///
/// * `input`   : 入力文字列
///
/// フィルタリングした残りの文字列
pub fn filter_time_word(mut input: &str) -> String {
    let mut words = vec![];

    loop {
        let mut flag = false;
        for &w in time_word() {
            if let Some(rest) = input.strip_prefix(w) {
                input = rest;
                words.push(w.to_string());
                flag = true;
                break;
            }
        }

        if flag {
            continue;
        }

        if !flag && input.len() == 0 {
            return words.join("");
        } else {
            let mut r = input.chars();
            r.next().unwrap();
            input = r.as_str();
            words.push(" ".to_string());
        }
    }
}

#[test]
fn test_split_time_word() {
    assert_eq!(
        filter_time_word("いい2/15ああ 16:30 aljdk"),
        String::from("  2/15   16:30      ")
    );
    assert_eq!(
        filter_time_word("2023/7/11の16:00"),
        String::from("2023/7/11 16:00")
    );
}

pub fn date_time_parser(input: &str) -> IResult<&str, (Date, Time)> {
    alt((
        tuple((date_parser, time_parser)),
        map(tuple((time_parser, date_parser)), |(time, date)| {
            (date, time)
        }),
    ))(input)
}

/// 時刻情報を解析するパーサー．日付と時間は順不同．
/// 確定していない項目はNoneとなる．例えば，「今日」
/// とだけ入力されたとすると，日付は確定できるが時間
/// は確定されない．従って日付の項目は全てSome(..)と
/// なるが，時間の項目は全てNoneとなる．
///
/// * `input`    : 入力文字列
///
/// 残りの文字列と解析した時刻情報を返す
pub fn get_date_time(input: &str) -> DateTime {
    let mut word: &str = &filter_time_word(input);
    let mut date = Date::new(None, None, None);
    let mut time = Time::new(None, None);

    loop {
        if word.len() <= 0 {
            return DateTime::new(date, time);
        }

        if !date.is_none() && !time.is_none() {
            return DateTime::new(date, time);
        }

        match date_parser(word) {
            Ok((rest, d)) => {
                date = d;
                word = rest;

                continue;
            }
            _ => {}
        }

        match time_parser(word) {
            Ok((rest, t)) => {
                time = t;
                word = rest;
                continue;
            }
            _ => {}
        }

        let mut chars = word.chars();
        chars.next();
        word = chars.as_str();
    }
}
