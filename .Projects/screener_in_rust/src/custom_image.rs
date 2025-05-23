use image::Pixel;
use scrap::{Capturer, Display};
use std::io::ErrorKind::WouldBlock;
use std::thread;
use std::time::Duration;
use image::{DynamicImage, GenericImageView, ImageBuffer, RgbaImage};
use crate::character_map::CharacterMap;

pub struct CustomImage {
    pub image: DynamicImage,
}

impl CustomImage {
    pub fn new() -> Self {
        CustomImage { image: DynamicImage::new_rgba8(0, 0) }
    }

    pub fn capture_screen(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        let display = Display::primary()?;
        let mut capturer = Capturer::new(display)?;
        let (w, h) = (capturer.width(), capturer.height());

        loop {
            match capturer.frame() {
                Ok(buffer) => {
                    let mut buf = Vec::with_capacity(w * h * 4);
                    let stride = buffer.len() / h;

                    for y in 0..h {
                        for x in 0..w {
                            let i = stride * y + 4 * x;
                            let b = buffer[i];
                            let g = buffer[i + 1];
                            let r = buffer[i + 2];
                            buf.push(r);
                            buf.push(g);
                            buf.push(b);
                            buf.push(255);
                        }
                    }

                    let img: RgbaImage = ImageBuffer::from_raw(w as u32, h as u32, buf).unwrap();
                    self.image = DynamicImage::ImageRgba8(img);
                    return Ok(());
                }
                Err(ref e) if e.kind() == WouldBlock => {
                    thread::sleep(Duration::from_millis(10));
                    continue;
                }
                Err(e) => return Err(Box::new(e)),
            }
        }
    }

    pub fn to_color_shape_map(&self, target_width: u32, target_height: u32) -> CharacterMap {
        let resized = self.image.resize_exact(
            target_width * 3,
            target_height * 3,
            image::imageops::FilterType::Triangle,
        );

        const OPAS: &str = " .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@";
        let opas_chars: Vec<char> = OPAS.chars().collect();

        let mut color_map = CharacterMap::new(target_width as usize, target_height as usize);

        for by in 0..target_height {
            for bx in 0..target_width {
                let mut gray_block = [0f32; 9];
                let mut total_r = 0u32;
                let mut total_g = 0u32;
                let mut total_b = 0u32;
                let mut idx = 0;

                for dy in 0..3 {
                    for dx in 0..3 {
                        let pixel = resized.get_pixel(bx * 3 + dx, by * 3 + dy).to_rgb();
                        let [r, g, b] = pixel.0;
                        total_r += r as u32;
                        total_g += g as u32;
                        total_b += b as u32;
                        gray_block[idx] = (r as f32 + g as f32 + b as f32) / 3.0;
                        idx += 1;
                    }
                }

                let avg_r = (total_r / 9) as u8;
                let avg_g = (total_g / 9) as u8;
                let avg_b = (total_b / 9) as u8;

                let mut best_index = 0;
                let mut best_dist = f32::MAX;

                for (si, shape) in CHARACTER_SHAPES.iter().enumerate() {
                    let mut dist = 0.0;
                    for i in 0..9 {
                        let diff = gray_block[i] - shape[i];
                        dist += diff * diff;
                    }
                    if dist < best_dist {
                        best_dist = dist;
                        best_index = si;
                    }
                }

                let ch = opas_chars[best_index % opas_chars.len()];
                let ansi = format!("\x1B[38;2;{};{};{}m{}", avg_r, avg_g, avg_b, ch);
                color_map.set(bx as usize, by as usize, ansi);
            }
        }

        color_map
    }
}

static CHARACTER_SHAPES: &[[f32; 9]] = &[
    [9.2,246.45,0.36,0.0,15.92,1.84,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0,0.0,0.0,146.16,0.0],
    [0.0,0.0,0.0,121.82,161.49,122.78,0.0,0.0,0.0],
    [0.0,151.87,0.0,0.0,143.26,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,148.64,0.0,0.0,145.96,0.0],
    [0.0,0.0,0.0,0.0,0.0,0.0,118.91,157.64,119.83],
    [0.0,0.0,0.0,0.0,0.0,0.0,0.0,314.2,0.0],
    [12.7,224.55,13.54,82.08,97.76,83.54,0.0,0.0,0.0],
    [0.0,0.0,0.0,243.37,322.61,245.28,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,148.52,0.0,0.0,314.19,0.0],
    [26.35,0.0,0.0,183.28,355.89,212.25,28.8,0.0,0.0],
    [0.0,0.0,26.04,205.27,339.49,181.82,0.0,0.0,28.37],
    [0.0,56.04,0.0,121.94,434.58,122.89,0.0,58.25,0.0],
    [0.0,142.66,0.0,0.0,259.75,0.0,0.0,146.03,0.0],
    [0.0,0.0,0.0,213.4,294.99,205.79,149.89,189.54,0.0],
    [0.0,0.0,0.0,292.51,176.27,127.7,87.63,177.65,94.9],
    [0.0,32.66,0.0,181.48,448.31,183.35,7.17,1.02,7.29],
    [0.0,27.57,205.16,8.76,325.21,27.76,174.45,56.14,0.0],
    [0.0,0.0,0.0,114.68,388.89,146.66,142.24,180.73,95.6],
    [115.79,178.18,99.57,1.81,223.96,111.66,0.0,146.75,0.0],
    [0.0,0.0,0.0,200.64,340.5,187.72,97.49,164.93,120.92],
    [141.99,0.0,0.0,354.36,0.0,0.0,153.27,161.6,122.99],
    [132.08,219.56,133.17,0.0,354.87,0.0,0.0,141.04,0.0],
    [0.0,0.0,0.0,271.61,143.52,273.5,9.09,230.46,9.73],
    [79.32,230.21,22.77,0.0,157.31,203.41,78.39,228.11,22.13],
    [0.0,127.84,164.43,73.54,0.0,354.94,126.97,163.48,101.78],
    [175.23,164.46,194.53,85.01,198.7,190.97,0.0,154.96,0.0],
    [21.78,229.87,80.33,199.77,160.49,0.0,21.13,227.67,79.27],
    [0.0,282.01,0.0,0.0,355.97,0.0,0.0,280.77,0.0],
    [146.51,164.26,133.25,359.35,164.61,59.0,141.14,0.0,0.0],
    [0.0,146.15,2.28,73.62,406.6,0.0,95.34,216.23,120.51],
    [0.0,252.76,69.87,57.29,386.48,0.0,0.0,253.06,68.84],
    [81.12,175.41,138.92,378.41,0.32,0.0,85.75,176.77,116.29],
    [69.11,253.45,0.0,0.0,385.16,58.54,68.13,254.27,0.0],
    [0.0,200.11,129.53,135.12,434.79,101.69,0.0,143.14,0.0],
    [96.0,219.73,96.76,0.0,355.92,0.0,94.45,217.33,95.2],
    [106.64,172.18,108.33,9.62,195.48,256.12,97.52,166.19,102.68],
    [92.58,197.85,0.0,0.35,356.42,0.0,93.74,217.35,103.29],
    [38.02,88.53,0.0,216.0,353.96,94.49,14.83,195.76,105.72],
    [122.97,184.7,0.0,0.0,358.25,0.0,0.0,188.76,106.37],
    [0.0,0.0,0.0,338.91,17.49,324.65,127.21,149.57,196.44],
    [32.98,295.25,82.78,49.03,306.97,0.0,32.68,292.54,81.89],
    [0.0,0.0,0.0,343.76,165.91,310.29,143.55,0.0,143.57],
    [0.0,0.0,0.0,314.37,314.31,251.41,93.04,170.07,77.21],
    [0.0,0.0,0.0,304.73,183.13,306.3,99.62,180.66,100.99],
    [103.5,171.6,159.64,48.24,301.93,49.94,156.44,169.05,110.64],
    [112.57,174.22,83.44,196.95,177.83,256.37,115.6,166.08,121.97],
    [147.31,0.0,147.42,93.71,381.18,95.15,0.0,141.12,0.0],
    [0.0,0.0,0.0,135.04,396.15,133.46,116.57,84.51,118.12],
    [0.0,98.22,50.01,55.67,306.91,143.23,91.83,302.23,91.82],
    [0.0,0.0,0.0,273.07,125.44,284.62,144.45,404.74,22.51],
    [0.0,0.0,0.0,194.09,337.25,222.76,149.58,140.1,189.13],
    [81.81,293.91,34.7,0.0,303.85,51.62,80.93,291.21,34.41],
    [118.18,173.61,93.31,8.13,190.84,203.74,152.24,194.2,113.1],
    [154.63,164.26,125.01,366.98,164.06,50.48,153.27,161.6,122.99],
    [105.71,169.41,99.07,150.37,206.65,162.71,112.26,161.5,116.47],
    [0.0,0.0,0.0,308.6,378.47,313.41,141.74,125.78,126.02],
    [0.0,0.0,0.0,322.79,152.33,342.28,128.18,147.14,356.14],
    [182.44,0.0,0.0,373.49,229.74,249.68,144.42,21.11,154.15],
    [154.46,166.4,122.55,366.9,166.5,280.66,140.83,0.0,0.0],
    [23.41,172.31,73.27,367.11,170.75,252.47,114.58,168.11,119.82],
    [181.15,0.0,0.0,367.78,158.5,310.16,143.41,0.0,143.43],
    [107.51,169.68,114.2,254.76,164.63,376.95,67.45,175.64,32.23],
    [0.0,0.0,181.11,324.52,154.12,371.54,130.12,152.26,147.31],
    [75.2,49.24,127.68,392.08,199.3,372.6,0.0,14.04,126.64],
    [144.75,0.0,144.76,250.69,187.88,252.93,7.61,235.89,8.32],
    [0.0,0.0,0.0,347.85,156.83,325.68,356.24,151.9,131.24],
    [109.78,172.04,110.76,368.24,0.0,368.43,111.88,169.2,112.93],
    [93.57,171.62,129.89,376.59,78.91,207.66,100.52,170.6,164.61],
    [181.18,0.0,0.0,368.5,158.05,325.87,157.32,160.45,86.76],
    [141.69,0.0,142.43,354.15,0.0,354.38,111.19,173.1,110.41],
    [5.01,231.47,5.43,250.13,353.43,253.17,140.3,0.0,140.31],
    [141.81,0.0,140.58,371.32,265.92,219.42,140.65,4.14,158.88],
    [142.54,20.09,142.93,70.82,487.91,72.8,139.75,22.52,140.57],
    [141.69,0.0,142.67,374.8,165.53,377.36,140.54,0.0,141.51],
    [0.0,0.0,0.0,354.73,349.75,361.41,143.43,123.06,144.87],
    [114.89,171.66,115.88,295.98,197.49,297.37,124.01,164.45,124.79],
    [162.54,167.11,119.27,374.66,217.61,295.9,140.54,5.33,154.13],
    [162.47,174.0,88.41,353.62,0.0,372.21,161.19,170.41,93.56],
    [40.13,96.11,105.08,322.6,428.49,326.77,102.71,95.09,41.22],
    [105.75,303.86,99.35,150.37,372.58,162.73,112.63,296.14,116.84],
    [154.46,170.67,100.67,366.9,173.03,305.02,153.26,163.47,149.51],
    [0.0,0.0,0.0,324.65,157.1,347.19,223.11,329.87,284.65],
    [93.8,179.68,95.14,366.59,156.06,365.96,95.96,176.56,97.18],
    [179.7,105.66,180.87,342.96,300.89,345.29,134.8,0.0,135.57],
    [170.54,51.81,142.24,360.13,280.92,359.05,141.51,50.96,170.1],
    [141.61,0.0,141.61,337.71,403.03,337.82,147.39,146.33,148.77],
    [109.78,172.04,110.76,368.32,0.0,368.25,111.99,347.85,200.46],
    [154.52,132.67,0.0,259.87,410.84,270.21,0.43,123.8,162.2],
    [85.36,187.22,89.1,315.45,268.92,200.51,157.23,176.94,171.74],
    [82.65,165.65,105.93,292.41,372.71,342.46,164.06,263.04,109.96],
];
