fn main() {
    let mut hh = 0;
    let mut hv = 0;
    let mut oh = 0;

    let mut lh: u32;
    let mut c: u32;
    let mut o: u32;
    let mut h: u32;
    for n in 1..=703 {
        lh = 0;
        c = n;
        o = 0;
        println!("c: {:5}, lh: {:5}", c, lh);
        h = loop {
            if c != 1 {
                if c % 2 == 0 {
                    c = c/2;
                } else {
                    c = 3*c + 1;
                }
                if lh< c {
                    lh = c;
                    println!("c: {:5}, lh: {:5}", c, lh);
                } else {
                    println!("c: {:5}, lh:  ----", c)
                }
                o += 1;
            } else {
                break lh;
            }
        };
        println!("\nHighest was: {h}\n\n\n\n");
        if hh< h {
            hh = h;
            hv = n;
            oh = o;
        }
    }
    println!("hh: {}, hv: {}, oh: {}", hh, hv, oh);
}