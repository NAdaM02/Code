use crate::character_map::CharacterMap;

pub fn make_axis((mx, my): (usize, usize), (sx, sy): (usize, usize)) -> CharacterMap {
    let width = (sx + 1)*(mx - 1) + 5;
    let height = (sy + 1)*(my - 1) + 5;
    let mut map = CharacterMap::new(width, height);

    for i in 0..width {
        let ch = if i == width - 1 { '>' } else if (i + 1) % (sx + 1) == 0 { '+' } else { '-' };
        map.array[height/2][i] = ch.to_string();
    }
    map.array[height/2 + 1][width - 1] = "x".to_string();

    let ycol = (mx/2)*(sx+1) + 2;
    for i in 0..height {
        let ch = if i == 0 { '^' } else if i % (sy + 1) == 0 { '+' } else { '|' };
        map.array[i][ycol] = ch.to_string();
    }
    map.array[0][ycol - 1] = "y".to_string();
    map
}

pub fn get_graph_marks<F>(func: F, (width, height): (usize, usize), (x0,x1): (f64, f64), (y0,y1): (f64, f64), marker: char) -> CharacterMap
where F: Fn(f64) -> f64 {
    let (x0,x1) = if x0==x1 {(-5.0, 5.0)} else {(x0,x1)};
    let (y0,y1) = if y0==y1 {(-5.0, 5.0)} else {(y0,y1)};
    let mut map = CharacterMap::new(width, height);
    let dx = (x1 - x0) / ((width - 1) as f64);

    for i in 0..width {
        let x = x0 + dx * (i as f64);
        let yv = func(x);
        let scaled = ((yv - y0) / (y1 - y0)) * ((height - 1) as f64);
        let gy = height - 1 - scaled.round() as usize;
        if gy < height {
            map.array[gy][i] = marker.to_string();
        }
    }
    map
}

pub fn make_graph<F>(func: F, size: (usize, usize), x_range: (f64,f64), y_range: (f64,f64), x_marks: (usize,usize), marker: char) -> CharacterMap
where F: Fn(f64) -> f64 {
    let (width, height) = size;
    let sx = (width - 5)/(x_marks.0) - 1;
    let sy = (height - 5)/(x_marks.1) - 1;
    let mut axis = make_axis(x_marks, (sx, sy));
    let marks = get_graph_marks(&func, (axis.width - 4, axis.height - 4), x_range, y_range, marker);

    for r in 0..marks.height {
        for c in 0..marks.width {
            let ch = &marks.array[r][c];
            if ch != " " {
                axis.array[r+2][c+2] = ch.clone();
            }
        }
    }
    axis
}
