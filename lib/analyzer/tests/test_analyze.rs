use analyzer::{analyze, data_time::DateTime, date::Date, time::Time, Operation, Response};

#[test]
fn test_analyze() {
    assert!(matches!(
        analyze("明日の１２時に面接の予定いれた"),
        Response {
            operation: Some(Operation::Add),
            date_time: DateTime {
                date: Date {
                    year: Some(_),
                    month: Some(_),
                    day: Some(_),
                },
                time: Time {
                    hour: Some(12),
                    minute: Some(0)
                }
            },
             title: Some(title),
        }
        if title == "面接".to_string()
    ));
    assert!(matches!(
        analyze("明日は５時起き"),
        Response {
            operation: Some(Operation::Add),
            date_time: DateTime {
                date: Date {
                    year: Some(_),
                    month: Some(_),
                    day: Some(_)
                },
                time: Time {
                    hour: Some(5),
                    minute: Some(0)
                }
            },
            title: Some(title),
        }
        if title == "起き".to_string()
    ));
    assert!(matches!(
        analyze("明日の予定は？"),
        Response {
            operation: Some(Operation::Search),
            date_time: DateTime {
                date: Date {
                    year: Some(_),
                    month: Some(_),
                    day: Some(_)
                },
                time: Time {
                    hour: None,
                    minute: None
                }
            },
            title: None,
        }
    ));
}