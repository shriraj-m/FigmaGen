// npm run watch 
// npm run build
figma.showUI(__html__);

figma.ui.onmessage = async (msg) => {
    if (msg.type === "send-prompt") {
        try {
            console.log('Attempting to send request to:', "http://localhost:8000/generate-ui/");
            console.log('Request payload:', { prompt: msg.prompt });
            
            const response = await fetch("http://localhost:8000/generate-ui/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ prompt: msg.prompt }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }

            const data = await response.json();
            console.log('Received response:', data);

            // Create elements based on the response
            const elements = data.elements;
            for (const element of elements) {
                if (element.type === "frame") {
                    const frame = figma.createFrame();
                    frame.resize(element.width, element.height);
                    frame.name = element.name;
                }
                else if (element.type === "text") {
                    const text = figma.createText();
                    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
                    text.characters = element.content;
                }
            }

            figma.ui.postMessage({ type: 'response', data });
            figma.notify("UI elements created successfully!");
            
        } catch (error) {
            console.error('Detailed error:', error);
            figma.ui.postMessage({ type: 'error', message: (error as Error).message });
        }
    } else if (msg.type === 'resize') {
        figma.ui.resize(msg.width, msg.height);
    }
};
