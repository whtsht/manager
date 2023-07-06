use analyzer::{title_op::get_title_and_op, Operation};

#[test]
fn test_get_title_and_op() {
    assert_eq!(
        get_title_and_op(
            vec!["予定".to_string(), "検索".to_string()],
            vec!["".to_string()],
            vec![]
        ),
        (None, Some(Operation::Search))
    );
    assert_eq!(
        get_title_and_op(
            vec!["資格".to_string(), "試験".to_string(), "予定".to_string()],
            vec![],
            vec![]
        ),
        (Some(String::from("資格試験")), None)
    );
    assert_eq!(
        get_title_and_op(
            vec!["面接".to_string(), "予定".to_string(), "追加".to_string()],
            vec![],
            vec![]
        ),
        (Some(String::from("面接")), Some(Operation::Add))
    );
    assert_eq!(
        get_title_and_op(vec!["資格".to_string(), "予定".to_string()], vec![], vec![]),
        (Some(String::from("資格")), None)
    );
    assert_eq!(
        get_title_and_op(vec![], vec![], vec!["は".to_string(), "?".to_string()]),
        (None, Some(Operation::Search))
    );
}
