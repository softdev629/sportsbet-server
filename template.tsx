import React from "react";

const TemplateTSX = () => {
  return (
    <main className="text-primaryfont">
      <div className="container px-3">
        <h1 className="font-bold font-primarybold mb-2 text-[2.75rem] tracking-tight">
          <<TITLE>>
        </h1>
        <h2 className="text-[26px] font-primary tracking-tight">
          <<DESCRIPTION>>
        </h2>
        <hr className="my-4 opacity-25" />
        <div className="flex mt-4 space-x-3">
          <div className="basis-7/12">
            <img
              className="mb-6"
              src="<<URLIMAGE>>"
            />
            <section className="font-secondary mb-2">
              <span>By </span>
              <span className="font-secondarybold text-primary">Nick</span>
            </section>
            <time
              className="font-secondary text-darkgrey"
              dateTime="2023-03-14T17:41:44.517Z"
            >
              <<DATETIME>>
            </time>
            <article className="text-primaryfont mt-4">
              <<ARTICLEDOM>>
            </article>
          </div>
          <div className="basis-1/12"></div>
          <div className="basis-1/3">
            <img
              className="mb-6"
              src="<<INTERCHANGE1>>"
            />
            <img
              className="mb-6"
              src="<<INTERCHANGE2>>"
            />
          </div>
        </div>
      </div>
    </main>
  );
};

export default TemplateTSX;
