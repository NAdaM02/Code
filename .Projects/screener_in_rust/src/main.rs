mod character_map;
mod terminal_display;
mod custom_image;
mod graph;

use clap::Parser;
use crate::terminal_display::TerminalDisplay;
use crate::custom_image::CustomImage;
use std::time::{Instant, Duration};
use std::io::{stdout, Write};
use crossterm::terminal;

#[derive(Parser)]
struct Args {
    p1: Option<String>,
}

fn figure_out_size(s: &str) -> Option<(usize, usize)> {
    if let Some(idx) = s.find(':') {
        let parts: Vec<&str> = s.split(':').collect();
        if parts.len() == 2 {
            if let (Ok(w), Ok(h)) = (parts[0].parse(), parts[1].parse()) {
                return Some((w, h));
            }
        }
    } else if let Ok(a) = s.parse::<usize>() {
        return Some((a*16, a*9));
    }
    None
}

fn main() {
    let args = Args::parse();
    let p1 = args.p1.unwrap_or_default();
    let mut width: Option<usize> = None;
    let mut height: Option<usize> = None;

    if let Some((w,h)) = figure_out_size(&p1) {
        width = Some(w);
        height = Some(h);
    }

    let terminal_height = height.unwrap_or(0);
    let terminal_display = TerminalDisplay::new(terminal_height);

    print!("\x1B[?25l");
    stdout().flush().unwrap();

    let mut last_time = Instant::now();
    loop {
        let mut cimg = CustomImage::new();
        cimg.capture_screen().expect("Screen capture failed");

        let display_map = if let (Some(w), Some(h)) = (width, height) {
            cimg.to_color_shape_map(w as u32, h as u32)
        } else {
            let (tw, th) = terminal::size().unwrap();
            let w = tw as usize;
            let h = th.saturating_sub(2) as usize;
            cimg.to_color_shape_map(w as u32, h as u32)
        };

        let now = Instant::now();
        let dt = now.duration_since(last_time).as_secs_f64();
        let fps = if dt > 0.0 { 1.0/dt } else { 0.0 };
        last_time = now;

        terminal_display.update(&display_map, 0.0);

        print!("\n\n\x1B[2K\x1B[38;2;55;55;55mFPS: \x1B[38;2;30;40;40m{:.0}", fps);
        stdout().flush().unwrap();

        std::thread::sleep(Duration::from_millis(16));
    }
}
