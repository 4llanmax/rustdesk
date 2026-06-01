import os

def patch_file(filepath):
    print(f"Patching submodule file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define all replacements
    replacements = [
        (
            'pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new("".to_owned());',
            'pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new(option_env!("RENDEZVOUS_SERVER").unwrap_or("").to_owned());'
        ),
        (
            'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
            'pub static ref APP_NAME: RwLock<String> = RwLock::new(option_env!("APP_NAME").unwrap_or("DottconDesk").to_owned());'
        ),
        (
            'pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = Default::default();',
            '''pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = {
        let mut m = HashMap::new();
        if let Some(srv) = option_env!("RENDEZVOUS_SERVER") {
            if !srv.is_empty() {
                m.insert("custom-rendezvous-server".to_string(), srv.to_string());
            }
        }
        if let Some(key) = option_env!("RS_PUB_KEY") {
            if !key.is_empty() {
                m.insert("key".to_string(), key.to_string());
            }
        }
        if let Some(api) = option_env!("API_SERVER") {
            if !api.is_empty() {
                m.insert("api-server".to_string(), api.to_string());
            }
        }
        RwLock::new(m)
    };'''
        ),
        (
            'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
            '''pub const RENDEZVOUS_SERVERS: &[&str] = &[
    match option_env!("RENDEZVOUS_SERVER") {
        Some("") => "rs-ny.rustdesk.com",
        Some(val) => val,
        None => "rs-ny.rustdesk.com",
    }
];'''
        ),
        (
            'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
            '''pub const RS_PUB_KEY: &str = match option_env!("RS_PUB_KEY") {
    Some("") => "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=",
    Some(val) => val,
    None => "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=",
};'''
        )
    ]

    patched = content
    for original, replacement in replacements:
        if original in patched:
            patched = patched.replace(original, replacement)
            print("Successfully patched a block!")
        else:
            print("Block already patched or not found!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patched)
    print("Submodule patch completed successfully!")

if __name__ == "__main__":
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_config = os.path.join(workspace, "libs", "hbb_common", "src", "config.rs")
    if os.path.exists(target_config):
        patch_file(target_config)
    else:
        print(f"Error: Could not find target config file at {target_config}")
