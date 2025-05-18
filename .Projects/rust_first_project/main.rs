use std::fmt;

struct Rgb(u8, u8, u8);



struct N{
    color:Rgb,
    owner:String,
}

struct W<'a>{
    goodness:u8,
    slaves:&'a[Box<&'a N>]
}

struct M{
    gardens_dug_up:u32,
    walls_jumped:u32
}



enum RS{
    W,
    N,
    M
}

impl fmt::Display for N {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let Rgb(r, g, b) = self.color;
        writeln!(f, "Color: ({} {} {})", r, g, b)?;
        writeln!(f, "Owner: {}", self.owner)?;
        write!(f, "")
    }
}

impl fmt::Display for W<'_> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "Goodness: {}", self.goodness)?;
        writeln!(f, "Slaves: ")?;
        for slave in self.slaves {
            let Rgb(r, g, b) = slave.color;
            writeln!(f, "  {} {} {}", r, g, b)?;
        }
        write!(f, "")
    }
}

impl fmt::Display for M {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "Gardens dug up: {}", self.gardens_dug_up)?;
        writeln!(f, "Walls jumped: {}", self.walls_jumped)?;
        write!(f, "")
    }
}

fn main() {    
    let n = N{color: Rgb(61, 42, 42), owner: "W".to_string()};
    let w = W{goodness: 100, slaves: &[Box::new(&n)]};
    let m = M{gardens_dug_up: 1, walls_jumped: 5};

    println!("> W:\n{w}\n\n");
    println!("> N:\n{n}\n\n");
    println!("> M:\n{m}\n\n");

    let r1 = RS::W;
    let _r2 = RS::N;
    let _r3 = RS::M;
    match r1 {
        RS::W => println!("good"),
        RS::N => println!("bad"),
        RS::M => println!("Just don't let them into the country.")
    }
}