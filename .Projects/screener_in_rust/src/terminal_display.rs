use std::io::{stdout, Write};
use crossterm::{queue, style::Print, terminal::{Clear, ClearType}};
use crossterm::cursor::MoveUp;
use crate::character_map::CharacterMap;

pub struct TerminalDisplay {
    pub height: usize,
}

impl TerminalDisplay {
    pub fn new(height: usize) -> Self {
        TerminalDisplay { height }
    }

    pub fn clear(&self) {
        let mut stdout = stdout();
        crossterm::execute!(stdout, Clear(ClearType::All)).unwrap();
    }

    pub fn to_beginning(&self) {
        let mut stdout = stdout();
        queue!(stdout, MoveUp((self.height + 2) as u16), Clear(ClearType::FromCursorDown)).unwrap();
        stdout.flush().unwrap();
    }

    pub fn write(&self, display_map: &CharacterMap) {
        let mut stdout = stdout();
        let mut out = String::new();
        for row in &display_map.array {
            for cell in row {
                out.push_str(cell);
            }
            out.push('\n');
        }
        queue!(stdout, Print(out)).unwrap();
        stdout.flush().unwrap();
    }

    pub fn update(&self, display_map: &CharacterMap, _fps: f64) {
        self.to_beginning();
        self.write(display_map);
    }
}
