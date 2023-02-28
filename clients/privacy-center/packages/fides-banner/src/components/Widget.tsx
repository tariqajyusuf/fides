import "./style.css";

type Props = {
  title?: string;
};

export const Widget = ({ title = "Default title" }: Props) => (
  <div id="fides-banner-widget">
    <h1>{title}</h1>
    <h2>Widget rendered</h2>
  </div>
);

export default Widget;
