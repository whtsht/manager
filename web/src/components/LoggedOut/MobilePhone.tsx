import "./mobile.css";

export default function MobilePhone({ src }: { src: string }) {
    return (
        <div className="sumaho-waku">
            <img src={src} style={{ maxHeight: "300px" }}></img>
        </div>
    );
}
