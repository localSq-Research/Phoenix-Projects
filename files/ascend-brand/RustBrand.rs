use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub enum AssetCategory {
    VisualIdentity,
    ApparelAndGear,
    DigitalAsset,
    Merchandise,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct BrandItem {
    pub id: u32,
    pub name: String,
    pub category: AssetCategory,
    pub description: String,
}

pub struct BrandInventory {
    items: Vec<BrandItem>,
}

impl BrandInventory {
    pub fn new() -> Self {
        let items = vec![
            // Visual Identity[span_5](start_span)[span_5](end_span)
            BrandItem {
                id: 1,
                name: "Ascend Global Logo".into(),
                category: AssetCategory::VisualIdentity,
                description: "Primary bird-arrow emblem with 'Innovate. Elevate. Succeed.' tagline[span_6](start_span)[span_6](end_span).".into(),
            },
            // Apparel & Gear[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span)
            BrandItem {
                id: 2,
                name: "Cycling Jersey & Bike".into(),
                category: AssetCategory::ApparelAndGear,
                description: "Teal and gold anime-styled character racing jersey and custom road bike[span_9](start_span)[span_9](end_span).".into(),
            },
            BrandItem {
                id: 3,
                name: "Branded Socks & Shoes".into(),
                category: AssetCategory::ApparelAndGear,
                description: "White cycling socks featuring the Ascend logo paired with performance shoes[span_10](start_span)[span_10](end_span).".into(),
            },
            // Digital Assets[span_11](start_span)[span_11](end_span)
            BrandItem {
                id: 4,
                name: "Gumroad P2P HTML Download".into(),
                category: AssetCategory::DigitalAsset,
                description: "P2P downloadable HTML package for community asset deployment[span_12](start_span)[span_12](end_span).".into(),
            },
            BrandItem {
                id: 5,
                name: "Discord Pinned Message Asset".into(),
                category: AssetCategory::DigitalAsset,
                description: "Optimized graphic layout for Discord channel #pinned-messages[span_13](start_span)[span_13](end_span).".into(),
            },
            // Merchandise[span_14](start_span)[span_14](end_span)
            BrandItem {
                id: 6,
                name: "Deskmat & Mousepad Set".into(),
                category: AssetCategory::Merchandise,
                description: "Gradient-styled office deskmat and matching mousepad[span_15](start_span)[span_15](end_span).".into(),
            },
            BrandItem {
                id: 7,
                name: "Notebook & Tote Bag".into(),
                category: AssetCategory::Merchandise,
                description: "Branded hardcover notebook and premium cotton tote bag[span_16](start_span)[span_16](end_span).".into(),
            },
        ];

        BrandInventory { items }
    }

    pub fn list_by_category(&self, category: AssetCategory) -> Vec<&BrandItem> {
        self.items.iter().filter(|i| std::mem::discriminant(&i.category) == std::mem::discriminant(&category)).collect()
    }
}

// Target Environment Execution
#[cfg(target_arch = "wasm32")]
use wasm_bindgen::prelude::*;

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(start))]
pub fn main() {
    let inventory = BrandInventory::new();

    #[cfg(target_arch = "wasm32")]
    {
        web_sys::console::log_str("Initialized Ascend Global Inventory for Firefox Focus WASM environment.");
    }

    #[cfg(not(target_arch = "wasm32"))]
    {
        println!("Running in Termux / Native CLI environment.");
        for item in &inventory.items {
            println!("- [{:?}] {}: {}", item.category, item.name, item.description);
        }
    }
}
