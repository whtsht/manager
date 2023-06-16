pub mod basic;
pub mod data_time;
pub mod date;
pub mod digits;
pub mod name_op;
pub mod time;

use data_time::DateTime;
use serde::Serialize;

#[derive(Debug, Serialize, PartialEq, Eq)]
pub enum Operation {
    Add,
    Search,
}

#[derive(Debug, Serialize, PartialEq, Eq)]
pub struct Response {
    pub title: Option<String>,
    pub operation: Option<Operation>,
    pub date_time: DateTime,
}

fn main() {
    println!("Hello, world!");
}
