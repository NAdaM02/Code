use std::cmp::{min, max};

pub struct CharacterMap {
    pub width: usize,
    pub height: usize,
    pub array: Vec<Vec<String>>,
    pub filler: String,
}

impl CharacterMap {
    pub fn new(width: usize, height: usize) -> Self {
        let filler = " ".to_string();
        let array = vec![vec![filler.clone(); width]; height];
        CharacterMap { width, height, array, filler }
    }

    pub fn fill(&mut self, fill: &str) {
        let filler = fill.to_string();
        for row in self.array.iter_mut() {
            for cell in row.iter_mut() {
                *cell = filler.clone();
            }
        }
        self.filler = filler;
    }

    pub fn add_map(&mut self, row: i32, col: i32, other: &CharacterMap, exclude: Option<&[&str]>) {
        let (self_h, self_w) = (self.height as i32, self.width as i32);
        let (other_h, other_w) = (other.height as i32, other.width as i32);
        let start_row = max(0, row);
        let end_row = min(self_h, row + other_h);
        let start_col = max(0, col);
        let end_col = min(self_w, col + other_w);

        for r in start_row..end_row {
            for c in start_col..end_col {
                let or = (r - row) as usize;
                let oc = (c - col) as usize;
                let ch = &other.array[or][oc];
                if let Some(excluded) = exclude {
                    if excluded.contains(&ch.as_str()) {
                        continue;
                    }
                }
                self.array[r as usize][c as usize] = ch.clone();
            }
        }
    }

    pub fn set(&mut self, x: usize, y: usize, val: impl ToString) {
        if x < self.width && y < self.height {
            self.array[y][x] = val.to_string();
        }
    }
}
