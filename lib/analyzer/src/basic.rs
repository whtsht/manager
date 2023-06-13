use nom::{
    branch::alt,
    bytes::complete::take_while,
    combinator::map,
    sequence::{preceded, terminated},
    IResult,
};

pub fn spaces(input: &str) -> IResult<&str, ()> {
    map(take_while(move |c| " 　\t\n".contains(c)), |_| ())(input)
}

pub fn char<'a>(target: char) -> impl FnMut(&'a str) -> IResult<&'a str, char> {
    preceded(
        spaces,
        terminated(nom::character::complete::char(target), spaces),
    )
}

pub fn tag<'a>(target: &'a str) -> impl FnMut(&'a str) -> IResult<&'a str, &'a str> {
    preceded(
        spaces,
        terminated(nom::bytes::complete::tag(target), spaces),
    )
}

pub fn one_of<'a>(target: &'a str) -> impl FnMut(&'a str) -> IResult<&'a str, char> {
    preceded(
        spaces,
        terminated(nom::character::complete::one_of(target), spaces),
    )
}

pub fn slash(input: &str) -> IResult<&str, char> {
    alt((char('/'), char('／')))(input)
}

pub fn colon(input: &str) -> IResult<&str, char> {
    alt((char(':'), char('：')))(input)
}
