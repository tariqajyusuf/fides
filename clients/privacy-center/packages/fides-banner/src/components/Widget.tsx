import { Counter } from "./Counter";

type Props = {
  title?: string;
};

export const Widget = ({ title = "Default title" }: Props) => (
  <div id="fides-banner-widget">
    <h1>{title}</h1>
    <h2>Widget rendered</h2>
    <Counter />
  </div>
);

export default Widget;
