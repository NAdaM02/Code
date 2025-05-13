fn main() {
    // Try changing the values in the array, or make it a slice!
    let array = [-1, 3, -2, 6];

    match array {
        [-1, n @ .., 6 ] => println!("First is -1, last is 6, and inbetween is {n:?}"),
        [.., 7] => println!("Last is 7, rest doesn't matter"),
        _ => println!("Nothing special.")
    }
}