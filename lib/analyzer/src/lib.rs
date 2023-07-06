//! Designer    : 東間日向
//! Date        : 2023/06/16
//! Purpose     : M14 変換関数と意味解析コンポーネントエントリーポイント

pub mod basic;
pub mod date;
pub mod date_time;
pub mod digits;
pub mod time;
pub mod title_op;

use crate::{date_time::time_word, title_op::get_title_and_op};
use date_time::{get_date_time, DateTime};
use mecab::Tagger;
use serde::Serialize;

/// 操作
#[derive(Debug, Serialize, PartialEq, Eq)]
pub enum Operation {
    /// 追加操作
    Add,
    /// 検索操作
    Search,
}

/// 変換処理で取り出す情報
#[derive(Debug, Serialize, PartialEq, Eq)]
pub struct Response {
    /// 予定名
    pub title: Option<String>,
    /// 操作
    pub operation: Option<Operation>,
    /// 時刻情報
    pub date_time: DateTime,
}

/// Jsonに変換可能な値をJsonに変換し文字列として返す
pub fn to_string<T: Serialize>(t: T) -> String {
    serde_json::to_string(&t).unwrap()
}

/// 文字列を解析し，予定名，操作，時刻情報を取り出す
pub fn analyze(input: &str) -> Response {
    let mut tagger = Tagger::new("-d /var/unidic");

    let mut noun = Vec::new();
    let mut verb = Vec::new();
    let mut hint = Vec::new();

    for node in tagger.parse_to_node(input).iter_next() {
        match node.stat as i32 {
            mecab::MECAB_BOS_NODE => {}
            mecab::MECAB_EOS_NODE => {}
            _ => {
                let word = &(node.surface)[..(node.length as usize)];
                if time_word().contains(&word) {
                    continue;
                }

                if &node.feature[0..6] == "名詞" {
                    noun.push(String::from(word));
                }
                if &node.feature[0..6] == "動詞" {
                    verb.push(String::from(word));
                }

                hint.push(String::from(word));
            }
        }
    }

    let (title, operation) = get_title_and_op(noun, verb, hint);

    let response = Response {
        title,
        operation,
        date_time: get_date_time(&input),
    };

    response
}
