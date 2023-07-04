//! Designer    : 東間日向
//! Date        : 2023/06/16
//! Purpose     : 操作名，予定名取得関数とその補助関数

use crate::Operation;
use once_cell::sync::Lazy;
use std::collections::HashSet;

/// 追加操作の文字列であるかどうかを返す
fn add_word(s: &str) -> bool {
    static WORD: Lazy<HashSet<&str>> =
        Lazy::new(|| HashSet::from_iter(["追加", "入る", "有る"].into_iter()));
    WORD.contains(s)
}

/// 追加操作の文字列であるかどうかを返す
fn search_word(s: &str) -> bool {
    static WORD: Lazy<HashSet<&str>> =
        Lazy::new(|| HashSet::from_iter(["参照", "検索", "教える"].into_iter()));
    WORD.contains(s)
}

/// 文字列から操作名，予定名を取り出す．
/// 予め操作に対応した文字列の集合を用意し，それらにマッチしたらそれを予定名とする．
///
/// * `noun`  - 名詞のリスト
/// * `verb`  - 動詞のリスト
/// * `hint`  - 名詞，動詞以外の単語のリスト
///
/// 予定名，操作を返す
pub fn get_title_and_op(
    noun: Vec<String>,
    verb: Vec<String>,
    hint: Vec<String>,
) -> (Option<String>, Option<Operation>) {
    let cond = |w: &String| !search_word(w) && !add_word(w) && w != "予定";
    let check_empty = |w: String| {
        if w.is_empty() {
            None
        } else {
            Some(w)
        }
    };

    if hint == vec!["使い", "方"] {
        return (None, None);
    }

    if ((hint.contains(&"?".into()) || hint.contains(&"？".into())) && hint.contains(&"は".into()))
        && hint.iter().filter(|w| add_word(w)).count() == 0
    {
        return (
            Some(noun.into_iter().filter(cond).collect()).and_then(check_empty),
            Some(Operation::Search),
        );
    }

    for op in noun.iter().chain(verb.iter()) {
        if search_word(&op) {
            return (
                Some(noun.into_iter().filter(cond).collect()).and_then(check_empty),
                Some(Operation::Search),
            );
        }

        if add_word(&op) {
            return (
                Some(noun.into_iter().filter(cond).collect()).and_then(check_empty),
                Some(Operation::Add),
            );
        }
    }

    (
        Some(noun.into_iter().filter(cond).collect()).and_then(check_empty),
        Some(Operation::Add),
    )
}
