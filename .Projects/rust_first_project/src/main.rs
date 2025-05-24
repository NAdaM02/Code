use std::sync::Arc;
use std::{borrow::Borrow, fmt, sync::Mutex};
use std::thread;

struct Rgb(u8, u8, u8);

struct SlaveData {
    color: Rgb,
    owner: String,
}

struct W<'a> {
    goodness: u8,
    slaves: &'a [Box<&'a SlaveData>],
}

struct SlaveDiggingStats {
    gardens_dug_up: u32,
    walls_jumped: u32,
}

enum SlaveInfo {
    W(),
    SimpleSlave(SlaveData),
    EfficientSlave(SlaveDiggingStats),
}

impl fmt::Display for SlaveData {
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

impl fmt::Display for SlaveDiggingStats {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "Gardens dug up: {}", self.gardens_dug_up)?;
        writeln!(f, "Walls jumped: {}", self.walls_jumped)?;
        write!(f, "")
    }
}

fn bombardillo_crodollio(items: Vec<SlaveDiggingStats>) {
    items
        .into_iter()
        .for_each(|item| println!("Heeellloo {}", item.gardens_dug_up))
}

fn penguinator_thermoregulator(items: Vec<&SlaveDiggingStats>) {
    items
        .into_iter()
        .for_each(|item| println!("Heeellloo {}", item.gardens_dug_up))
}

fn asd<T: Borrow<SlaveDiggingStats>>(items: Vec<T>) {
    items
        .into_iter()
        .for_each(|item| println!("Heeellloo {}", item.borrow().gardens_dug_up))
}

fn main() {
    let n = SlaveData {
        color: Rgb(61, 42, 42),
        owner: "White".to_string(),
    };
    let w = W {
        goodness: 100,
        slaves: &[Box::new(&n)],
    };

    let m = SlaveDiggingStats {
        gardens_dug_up: 1337,
        walls_jumped: 42,
    };

    let v1 = SlaveInfo::SimpleSlave(n);
    let a = Arc::new(Mutex::new(v1));

    for i in 1..=100 {
        let counter_clone = Arc::clone(&a);

        thread::spawn(move || {
            let res = counter_clone.lock().unwrap();
            let szar = &*res;

            match szar {
                SlaveInfo::SimpleSlave(D) => println!("🧵 {}", &D.owner),
                _ => (),
            }
        });

        
    }
    
    /*

    println!("> W:\n{w}\n\n");
    println!("> N:\n{n}\n\n");
    println!("> M:\n{m}\n\n");

    let r1 = RS::W;
    let _r2 = RS::N;
    let _r3 = RS::M;
    match r1 {
        RS::W => println!("good"),
        RS::N => println!("bad"),
        RS::M => println!("Just don't let them into the country."),
    }
    */
}