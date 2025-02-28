// import React from "react";

// const Input = ({ type = "text", placeholder, value, onChange }) => {
//     return (
//         <input
//             type={type}
//             placeholder={placeholder}
//             value={value}
//             onChange={onChange}
//             className="border border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
//         />
//     );
// };

// export default Input;



const Input = ({ type, placeholder, value, onChange }) => {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className="p-2 border rounded-md w-full"
        />
    );
};

export default Input; // ✅ Default export
