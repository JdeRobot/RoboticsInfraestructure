#!/bin/bash

# Function to get the GPU device path based on vendor priority
get_gpu_device() {
    preferred_vendor=$1
    # Default vendor priority: NVIDIA > AMD > Intel
    priority=(nvidia amd intel)

    # If a preferred vendor is provided, prioritize it
    if [ -n "$preferred_vendor" ]; then
        priority=("$preferred_vendor")
    fi

    # Get GPU information
    gpu_list=$(lspci -nn -D| grep -E "VGA|3D controller")
    echo "GPUs found:"
    echo "$gpu_list" | while IFS= read -r line; do
        echo -e "\t$line"
    done

    for vendor in "${priority[@]}"; do
        if [[ "$vendor" == "nvidia" ]]; then
            # Check if nvidia-smi works
            if ! command -v nvidia-smi &> /dev/null || ! nvidia-smi &> /dev/null; then
                echo "Warning: nvidia-smi not available or failed, skipping NVIDIA GPU." >&2
                continue
            fi
        fi

        # Search for the vendor in the GPU list from lspci
        gpu_info=$(echo "$gpu_list" | grep -i "$vendor" | head -n 1)
        if [ -n "$gpu_info" ]; then
            bus=$(echo "$gpu_info" | cut -d' ' -f1)
            device=$(ls /sys/bus/pci/devices/$bus/drm | grep card)

            # Check if corresponding dri path exists
            device_path="/dev/dri/$device"
            if [ ! -e $device_path ]; then
                echo "Warning: Skipping $device_path does not exist."
                continue
            fi

            if [ -n "$device" ]; then
                # Set the DRI_NAME environment variable to the card name (e.g., card0, card1)
                export DRI_NAME="$device"
                export DRI_VENDOR="$vendor"

                # Echo the selected vendor and DRI_NAME
                echo "GPU selected:"
                echo -e "\t$gpu_info"
                echo -e "\tDRI_VENDOR: $DRI_VENDOR"
                echo -e "\tDRI_NAME: $DRI_NAME"
                return 0
            fi
        fi
    done


    if [ -n "$preferred_vendor" ]; then
        echo "Warning: No GPU found for requested vendor '$preferred_vendor'"
    else
        echo "Warning: No GPU found for valid vendors: '${priority[@]}'"
    fi
    echo "Falling back to CPU-only mode"

    return 1
}

# Check if a preferred vendor is passed as an argument
preferred_vendor="${1,,}"  # Convert to lowercase

# Get the GPU device path based on priority and set DRI_NAME
echo -e "\n--- GPU acceleration info ---"
get_gpu_device "$preferred_vendor"
echo -e "-----------------------------\n"
