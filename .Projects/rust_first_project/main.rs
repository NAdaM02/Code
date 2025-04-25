fn main() {
    let mut c: u32 = 0;
    let m: u32 = u32::MAX;
    while c != m {
        c += 1;
    }
    println!("Limit reached");
}