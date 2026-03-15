#[kani::proof]
fn verify_update_bounds() {
    let update: f32 = kani::any();
    
    // We call our aggregation logic
    let result = safe_aggregate(update);
    
    // Mathematically prove the result is always within safe bounds
    assert!(result >= -1.0 && result <= 1.0);
}

fn safe_aggregate(val: f32) -> f32 {
    // Handle the NaN bug discovered in the previous run
    if val.is_nan() {
        return 0.0; 
    }
    if val > 1.0 {
        return 1.0;
    } else if val < -1.0 {
        return -1.0;
    }
    val
}

fn main() {
    println!("Aggregator logic ready for verification.");
}
