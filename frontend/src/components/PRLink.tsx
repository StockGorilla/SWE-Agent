import React from "react";

interface Props {
  url: string;
}

const PRLink: React.FC<Props> = ({ url }) => (
  <a href={url} target="_blank" className="inline-block mt-3 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
    View Pull Request
  </a>
);

export default PRLink;
