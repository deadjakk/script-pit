use isahc::prelude::*;
use std::error::Error;
use structopt::StructOpt;
use std::io::{BufReader,BufRead};
use std::fs::File;

#[derive(Debug,StructOpt)]
struct Opt {
    /// URL to inject 
    /// must contain a '*' at the point of injection
    #[structopt(short,long,required=true)]
    url: String,
    /// File contaiing tests to run
    /// These will be placed in the injection point
    #[structopt(short,long,required=true)]
    file: String,
}

fn main() -> Result<(),Box<dyn Error>>{
    let args = Opt::from_args();
    let fmt_url = format!("{}",args.url);
    if fmt_url.matches("*").count() == 0 {
        eprintln!("provided url must include an injection point as: *");
        std::process::exit(1);
    }
    let tests = BufReader::new(File::open(args.file)?).lines().collect::<Vec<_>>();
    for test in tests {
        let url = fmt_url.replace("*",&test.unwrap());
        print!("T: {}",url);

        let response = isahc::get(url);
        match response {
            Ok(mut response) =>  println!("\n\tR {:?}", response.text().unwrap().to_string()),
            Err(e) => println!("\n\tE {}", e.to_string()),
        }
    }
    Ok(())
}
