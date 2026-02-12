export default function ResponseViewer({ response }) {
    if (!response) return null;

    return (
        <pre
            style={{
                marginTop: "20px",
                padding: "10px",
                background: "#f5f5f5",
                borderRadius: "5px",
            }}
        >
            {JSON.stringify(response, null, 2)}
        </pre>
    );
}
