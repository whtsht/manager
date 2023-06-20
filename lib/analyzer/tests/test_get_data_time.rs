use analyzer::{
    data_time::{get_date_time, DateTime},
    date::Date,
    time::Time,
};

#[test]
fn test_get_data_time() {
    assert_eq!(
        get_date_time("2023年6月12日14:16"),
        DateTime {
            date: Date {
                year: Some(2023),
                month: Some(6),
                day: Some(12),
            },
            time: Time {
                hour: Some(14),
                minute: Some(16),
            }
        }
    );
    assert!(matches!(
        get_date_time("今日"),
        DateTime {
            date: Date {
                year: Some(..),
                month: Some(..),
                day: Some(..)
            },
            time: Time {
                hour: None,
                minute: None
            }
        }
    ));
}
