use std::env;

use analyzer::{analyze, to_string};

/// C2 意味解析のエントリーポイント．入力はコマンドライン引数として渡す
fn main() {
    let mut args = env::args();

    if let Some(input) = args.nth(1) {
        println!("{}", to_string(analyze(&input)));
    } else {
        println!("Argument expected");
    }
}
