// npm run watch 
// npm run build
figma.showUI(__html__);

interface FigmaElement {
    type: string;
    name?: string;
    width?: number;
    height?: number;
    x?: number;
    y?: number;
    fills?: any[];
    strokes?: any[];
    effects?: any[];
    characters?: string;
    fontSize?: number;
    fontName?: FontName;
    textAlignHorizontal?: string;
    textAlignVertical?: string;
    cornerRadius?: number;
    children?: FigmaElement[];
    constraints?: any;
    layoutMode?: string;
    primaryAxisSizingMode?: string;
    counterAxisSizingMode?: string;
    paddingLeft?: number;
    paddingRight?: number;
    paddingTop?: number;
    paddingBottom?: number;
    itemSpacing?: number;
    style?: {
        textAlignHorizontal?: string;
        fills?: any[];
    };
    [key: string]: any;
}

async function createComponent(element: FigmaElement) {
    try {
        console.log('Creating component:', element);
        let node;

        switch (element.type) {
            case "FRAME":
                node = figma.createFrame();
                if (element.layoutMode) {
                    node.layoutMode = element.layoutMode as "HORIZONTAL" | "VERTICAL";
                    node.primaryAxisSizingMode = (element.primaryAxisSizingMode || "AUTO") as "FIXED" | "AUTO";
                    node.counterAxisSizingMode = (element.counterAxisSizingMode || "AUTO") as "FIXED" | "AUTO";
                    if (element.itemSpacing) node.itemSpacing = element.itemSpacing;
                    if (element.paddingLeft) node.paddingLeft = element.paddingLeft;
                    if (element.paddingRight) node.paddingRight = element.paddingRight;
                    if (element.paddingTop) node.paddingTop = element.paddingTop;
                    if (element.paddingBottom) node.paddingBottom = element.paddingBottom;
                }
                break;

            case "RECTANGLE":
                node = figma.createRectangle();
                if (element.cornerRadius) {
                    node.cornerRadius = element.cornerRadius;
                }
                break;

            case "TEXT":
                // Load font first, before creating any text nodes
                await figma.loadFontAsync({ family: "Inter", style: "Regular" });

                // Now create the text node and set properties
                const text = figma.createText();
                if (element.name) text.name = element.name;
                text.resize(element.width || 100, element.height || 50);
                text.x = element.x || 0;
                text.y = element.y || 0;

                // Set text properties
                text.characters = element.characters || " ";
                text.fontSize = element.fontSize || 14;
                if (element.style?.textAlignHorizontal) {
                    text.textAlignHorizontal = element.style.textAlignHorizontal as "LEFT" | "CENTER" | "RIGHT";
                }
                if (element.style?.fills) text.fills = element.style.fills;
                
                node = text;
                break;

            case "GROUP":
                node = figma.group([], figma.currentPage);
                break;

            case "ELLIPSE":
                node = figma.createEllipse();
                break;

            case "LINE":
                node = figma.createLine();
                break;

            case "VECTOR":
                node = figma.createVector();
                break;

            default:
                console.warn(`Unsupported element type: ${element.type}`);
                return null;
        }

        if (node) {
            // Apply common properties
            if (element.name) node.name = element.name;
            if (element.x) node.x = element.x;
            if (element.y) node.y = element.y;
            if (element.width) node.resize(element.width, element.height || element.width);

            // Check node type before applying style properties
            if ('fills' in node && element.fills) node.fills = element.fills;
            if ('strokes' in node && element.strokes) node.strokes = element.strokes;
            if ('effects' in node && element.effects) node.effects = element.effects;
            if ('constraints' in node && element.constraints) node.constraints = element.constraints;

            // Handle children only for container nodes
            if ('appendChild' in node && Array.isArray(element.children) && element.children.length > 0) {
                for (const child of element.children) {
                    const childNode = await createComponent(child);
                    if (childNode) {
                        node.appendChild(childNode);
                    }
                }
            }

            return node;
        }

    } catch (error) {
        console.error('Error creating component:', error);
        throw error;
    }
    return null;
}

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

            if (!data || !data.elements || !Array.isArray(data.elements)) {
                throw new Error('Invalid response format from server');
            }

            for (const element of data.elements) {
                if (element) {
                    await createComponent(element);
                }
            }

            figma.ui.postMessage({ type: 'response', data });
            figma.notify("UI elements created successfully!");
            
        } catch (error) {
            console.error('Detailed error:', error);
            figma.ui.postMessage({ type: 'error', message: error instanceof Error ? error.message : 'Unknown error' });
        }
    } else if (msg.type === 'resize') {
        figma.ui.resize(msg.width, msg.height);
    }
};
