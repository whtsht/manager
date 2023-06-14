//! Designer    : 東間日向
//! Date        : 2023/06/13
//! Purpose     : 数字を解析するパーサー群

use crate::basic::{char, one_of};
use nom::{
    branch::alt,
    combinator::map,
    multi::{many0, many1},
    sequence::tuple,
    IResult,
};

/// アラビア数字を大文字から小文字に変換する
fn upper_to_digit(s: char) -> char {
    match s {
        '１' => '1',
        '２' => '2',
        '３' => '3',
        '４' => '4',
        '５' => '5',
        '６' => '6',
        '７' => '7',
        '８' => '8',
        '９' => '9',
        '０' => '0',
        _ => unreachable!(),
    }
}

/// 漢数字から小文字に変換する
fn kanzi_to_digit(s: char) -> u32 {
    match s {
        '一' => 1,
        '二' => 2,
        '三' => 3,
        '四' => 4,
        '五' => 5,
        '六' => 6,
        '七' => 7,
        '八' => 8,
        '九' => 9,
        '〇' => 0,
        _ => unreachable!(),
    }
}

/// 漢数字を一文字解析するパーサー
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
fn kanzi_digit_with0(input: &str) -> IResult<&str, u32> {
    map(one_of("一二三四五六七八九〇"), kanzi_to_digit)(input)
}

/// 一九八五のような単純な漢数字を解析するパーサー
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
pub fn simple_kanzi_digits(input: &str) -> IResult<&str, u32> {
    alt((
        map(
            tuple((
                map(one_of("一二三四五六七八九"), kanzi_to_digit),
                map(many0(one_of("一二三四五六七八九〇")), |v| {
                    v.into_iter().map(kanzi_to_digit).collect::<Vec<_>>()
                }),
            )),
            |(a, mut b)| {
                let mut m = 1;
                let mut sum = 0;
                while let Some(e) = b.pop() {
                    sum += e * m;
                    m *= 10;
                }
                sum += a * m;
                sum
            },
        ),
        map(char('〇'), |_| 0),
    ))(input)
}

/// 千九百八十五のような複雑な漢数字を解析するパーサー
///
/// * `input`  - 先頭に漢数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
pub fn complex_kanzi_digits(input: &str) -> IResult<&str, u32> {
    fn zyu(input: &str) -> IResult<&str, u32> {
        alt((
            map(
                tuple((kanzi_digit_with0, char('十'), kanzi_digit_with0)),
                |(z, _, i)| z * 10 + i,
            ),
            map(tuple((char('十'), kanzi_digit_with0)), |(_, i)| i + 10),
            map(char('十'), |_| 10),
        ))(input)
    }

    fn hyaku(input: &str) -> IResult<&str, u32> {
        alt((
            map(tuple((kanzi_digit_with0, char('百'), zyu)), |(h, _, z)| {
                h * 100 + z
            }),
            map(tuple((char('百'), zyu)), |(_, z)| z + 100),
            map(char('百'), |_| 100),
            zyu,
        ))(input)
    }

    fn sen(input: &str) -> IResult<&str, u32> {
        alt((
            map(
                tuple((kanzi_digit_with0, char('千'), hyaku)),
                |(h, _, z)| h * 1000 + z,
            ),
            map(tuple((char('千'), hyaku)), |(_, z)| z + 1000),
            map(char('千'), |_| 1000),
            hyaku,
        ))(input)
    }

    alt((sen,))(input)
}

/// アラビア数字を解析するパーサー
///
/// * `input`  - 先頭にアラビア数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
pub fn numeric_digits(input: &str) -> IResult<&str, u32> {
    let ascii = one_of("1234567890");
    let upper = one_of("１２３４５６７８９０");

    map(
        many1(alt((ascii, map(upper, upper_to_digit)))),
        |v| match &v[..] {
            ['0'] => 0,
            v => v
                .into_iter()
                .filter(|&&c| c != '0')
                .collect::<String>()
                .parse()
                .unwrap(),
        },
    )(input)
}

/// アラビア数字，漢数字を解析するパーサー．大文字の数字も解析可能
///
/// * `input`  - 先頭に数字を含む文字列
///
/// 残りの文字列と解析した数値を返す
pub fn digits(input: &str) -> IResult<&str, u32> {
    alt((numeric_digits, complex_kanzi_digits, simple_kanzi_digits))(input)
}

#[cfg(test)]
mod tests {
    use super::digits;

    #[test]
    fn test_digits_ok() {
        // 単純な漢数字
        assert_eq!(digits("二三九五"), Ok(("", 2395)));
        assert_eq!(digits("一一〇"), Ok(("", 110)));
        assert_eq!(digits("〇六四"), Ok(("六四", 0)));

        // 複雑な漢数字
        assert_eq!(digits("二千十三"), Ok(("", 2013)));
        assert_eq!(digits("千千二十三"), Ok(("千二十三", 1000)));

        // アラビア数字
        assert_eq!(digits("43892は"), Ok(("は", 43892)));
        assert_eq!(digits("0293"), Ok(("", 293)));
        assert_eq!(digits("0"), Ok(("", 0)));
    }

    #[test]
    fn test_digits_err() {
        // 先頭が数字でないならばエラー
        assert!(digits("饅頭2390").is_err());
    }
}
