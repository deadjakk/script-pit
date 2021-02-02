use websocket::client::ClientBuilder;
use websocket::{OwnedMessage,Message};
use structopt::StructOpt;

#[derive(StructOpt,Debug)]
struct Opt{
    /// Target endpoint
    /// Example: "getStuff"
    #[structopt(short,long)]
    endpoint: String,

    /// URL, including the protocol but excluding the endpoint and trailing slash
    /// Example: "https://wsserverhost"
    #[structopt(short,long)]
    host: String,

    /// Payload to send
    /// Example: {"data":"items"}
    #[structopt(short,long)]
    data: String,

    /// Quiet, show only length
    #[structopt(short,long)]
    quiet: bool
}

fn main() {
    let opts = Opt::from_args();
    let mut client = ClientBuilder::new(&format!("{}/{}",&opts.host,&opts.endpoint)).unwrap();
    println!("connected");
    let mut stream = client.connect_secure(None).unwrap();
    if let Err(e) = stream.send_message(&Message::text(&opts.data)){
        eprintln!("error sending msg: {:?}",e);
        return;
    }
    println!("sent message.");
    match stream.recv_message(){
        Ok(resp)=> {
            match resp{
                OwnedMessage::Text(text)=>{
                    if !opts.quiet{
                        println!("text response:{:?}",text);
                    }
                    println!("text length:{}",text.len());
                }
                OwnedMessage::Binary(bin)=>{
                    if !opts.quiet{
                        println!("binary response:{:?}",bin);
                    }
                    println!("bin length:{}",bin.len());
                }
                _ =>{
                    println!("other response received:{:?}",resp);
                }
            }
        }
        Err(e)=>eprintln!("error receiving message:{:?}",e),
    }
}
