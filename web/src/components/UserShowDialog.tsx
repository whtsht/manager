// /**
//  * Designer    : 菊地智遥
//  * Date        : 2023/6/
//  * Purpose     : test
//  */

import liff from "@line/liff";
import { useState, useEffect } from "react";
import DialogTitle from "@mui/material/DialogTitle";
import Dialog from "@mui/material/Dialog";
import { Button } from "@mui/material";
import React from "react";
import loggedOut from "./loggedOut";

async function getNameAndIcon(): Promise<
  [string | undefined, string | undefined]
> {
  const obj = await liff.getDecodedIDToken();
  return [obj?.name, obj?.picture];
}

function isLoggedIn(): boolean {
  let ret = false;
  try {
    ret = liff.isLoggedIn();
  } catch (e) {
    console.log(e);
  }
  return ret;
}

// /**
//  * Appサーバーに対して，HTTPリクエストを送信する．
//  *
//  * @param lineID   - ユーザーのLineID
//  * @returns
//  */

function UserShowDialog({ lineID }: { lineID: string }) {
  const [name, setName] = useState<undefined | string>(undefined);
  const [icon, setIcon] = useState<undefined | string>(undefined);
  useEffect(() => {
    (async () => {
      if (isLoggedIn()) {
        const [name_, icon_] = await getNameAndIcon();
        setName(name_);
        setIcon(icon_);
      }
    })();
  }, []);

  const handleClose = () => {
    // onClose(selectedValue);
  };

  const handleListItemClick = (value: string) => {
    // onClose(value);
  };

  const [open, setOpen] = React.useState(true);

  return (
    <Dialog onClose={handleClose} open={open}>
      <img
        src="https://profile.line-scdn.net/0hI7RALfkSFhhvOAHiYxVpT1N9GHUYFhBQF1hRLR45HC5GAFcbUVkJfk5oTn1CX1FGVFwMKkw5SXhC"
        alt="アイコン"
        style={{
          borderRadius: "50%",
          width: "180px",
          height: "180px",
          padding: "20px",
        }}
      />
      <h1>{name}</h1>
      <Button
        variant="outlined"
        onClick={() => {
          if (liff.isLoggedIn()) {
            liff.logout();
            window.location.reload();
          }
          setOpen(false);
        }}
      >
        ログアウト
      </Button>
    </Dialog>
  );
}

export default UserShowDialog;

// import DialogTitle from "@mui/material/DialogTitle";
// import Dialog from "@mui/material/Dialog";
// import { Button } from "@mui/material";
// import React from "react";

// export interface SimpleDialogProps {
//   open: boolean;
//   selectedValue: string;
//   onClose: (value: string) => void;
// }

// export default function UserShowDialog() {
//   const handleClose = () => {
//     // onClose(selectedValue);
//   };

//   const handleListItemClick = (value: string) => {
//     // onClose(value);
//   };

//   const [open, setOpen] = React.useState(true);

//   return (
//     <Dialog onClose={handleClose} open={open}>
//       <img src = icon_ alt = "アイコン"/>
//       <h1>name_</h1>
//       <Button
//         variant="outlined"
//         onClick={() => {
//           if(liff.isLoggedIn()){
//             liff.logout();
//             window.location.reload();
//           }
//           setOpen(false);
//         }}
//       >
//         ログアウト
//       </Button>
//     </Dialog>
//   );
// }
