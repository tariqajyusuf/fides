import styles from "./styles.css";

type Props = {
  title?: string;
};

console.log(">>> styles", styles);

export const Widget = ({ title = "Default title" }: Props) => (
  <div id="fides-banner-widget" className={styles.fidesBannerWidget}>
    <h1>{title}</h1>
    <h2>Widget rendered</h2>
  </div>
);

export default Widget;
