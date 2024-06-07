import tkinter as tk
from tkinter.font import Font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from typing import Iterator, Self
from enum import IntEnum, auto
from dataclasses import dataclass


__all__ = [
    "TextExplainSimilarCharacters",
]


class CharacterType(IntEnum):
    """文字の種類
    """
    # 通常文字
    DEFAULT = auto()
    # 類似文字
    SIMILAR = auto()
    # 類似文字の説明
    EXPLAIN = auto()

    def __str__(self) -> str:
        if self is CharacterType.DEFAULT:
            return "default"
        elif self is CharacterType.SIMILAR:
            return "similar"
        elif self is CharacterType.EXPLAIN:
            return "explain"
        else:
            assert False, "not support"


@dataclass(frozen=True)
class InsertData:
    """insert関数に突っ込むデータ
    """
    # 文字列
    chars:str
    # タグ名
    tag:str

    def __iter__(self) -> Iterator[str]:
        return iter((self.chars, self.tag))


@dataclass(frozen=True)
class CharacterData:
    """文字情報
    """
    # 1列にした場合の位置
    index:int
    # 行位置
    row:int
    # 列位置
    column:int
    # 文字
    character:int
    # 文字の種類
    ctype:CharacterType

    def __lt__(self, rhs:Self) -> bool:
        return self.index < rhs.index

    def __iter__(self) -> Iterator[int]:
        return iter((self.row, self.column))

    def __str__(self) -> str:
        return f"{self.row}.{self.column}"


@dataclass
class IndexData:
    """インデックスデータ
    """
    # 行位置
    row:int
    # 列位置
    column:int

    def __str__(self) -> str:
        return f"{self.row}.{self.column}"

    def __iter__(self) -> Iterator[int]:
        return iter((self.row, self.column))

    @classmethod
    def from_index(cls, index:str) -> Self:
        return cls(*[int(value) for value in index.split(".")])


class TextExplainSimilarCharacters(ttk.Text):
    """類似文字を説明するテキスト
    """
    def __init__(
        self,
        master:tk.Misc,
        width:int = 80,
        height:int = 4,
        family:str = "MotoyaLMaru",
        size:int = 18,
        spacing1:int = 10,
        spacing2:int = 10,
        spacing3:int = 10,
    ) -> None:
        """コンストラクタ

        Args:
            master (tk.Misc): master
            width (int, optional): 表示幅. Defaults to 80.
            height (int, optional): 表示行数. Defaults to 4.
            family (str, optional): フォント名. Defaults to "MotoyaLMaru".
            size (int, optional): フォントサイズ. Defaults to 18.
            spacing1 (int, optional): 最初の行の上のスペース. Defaults to 10.
            spacing2 (int, optional): 行間の間隔. Defaults to 10.
            spacing3 (int, optional): 最後の行の後のスペース. Defaults to 10.
        """
        super().__init__(master, width=width)

        # 文字の種類ごとのフォント設定
        self.default_font = Font(self, family=family, size=size, weight="normal")
        self.similar_font = Font(self, family=family, size=size, weight="normal")
        self.explain_font = Font(self, family=family, size=size//2, weight="normal")

        # 文字の種類ごとのフォント設定を登録
        self.tag_configure(CharacterType.DEFAULT, font=self.default_font)
        self.tag_configure(CharacterType.SIMILAR, font=self.similar_font)
        self.tag_configure(CharacterType.EXPLAIN, font=self.explain_font, offset=size//2)

        # 初期設定の変更
        self.configure(font=self.default_font, height=height, spacing1=spacing1, spacing2=spacing2, spacing3=spacing3)

        # 類似文字と説明
        self.similar_character_and_explain_table:dict[str, str] = {
            "ロ": "カタカナ",
            "口": "漢字",
            "ー": "長音符",
            "一": "漢数字",
            "－": "記号",
            "カ": "カタカナ",
            "力": "漢字",
            "エ": "カタカナ",
            "工": "漢字",
            "十": "漢数字",
            "＋": "記号",
            "ｘ": "小文字",
            "×": "記号",
            "ニ": "カタカナ",
            "二": "漢数字",
            "へ": "ひらがな",
            "ヘ": "カタカナ",
            "べ": "ひらがな",
            "ベ": "カタカナ",
            "ぺ": "ひらがな",
            "ペ": "カタカナ",
        }

        # register callbacks
        self.bind("<Control-c>", self.on_copy)
        self.bind("<Control-v>", self.on_paste)
        self.bind("<Control-x>", self.on_cut)
        self.bind("<BackSpace>", self.on_backspace)
        self.bind("<Delete>", self.on_delete)
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)

    def on_copy(self, event:tk.Event) -> str:
        """類似文字説明を除いたコピー

        Args:
            event (tk.Event): イベントプロパティ

        Returns:
            str: "break"
        """
        try:
            first, last = self.get_sel()

            # 選択範囲の文字情報リストを取得
            character_data_list = self.get_character_data_list()
            character_data_list = character_data_list[self.row_n_column_to_index(character_data_list, *first):self.row_n_column_to_index(character_data_list, *last)]

            # 選択範囲から類似文字説明を除いたテキストを作成
            text = "".join((character_data.character for character_data in character_data_list if character_data.ctype is not CharacterType.EXPLAIN))

            self.clipboard_clear()
            self.clipboard_append(text)
        except Exception as e:
            # 全コピー
            self.clipboard_clear()
            self.clipboard_append(self.get_text())

        return "break"

    def on_paste(self, event:tk.Event) -> str:
        """貼り付け

        Args:
            event (tk.Event): イベントプロパティ

        Returns:
            str: "break"
        """
        try:
            # Ctrl押下時(on_key_press)に選択範囲の修正は完了しているので素直に削除します。
            first, last = self.get_sel()
            self.delete(first, last)
        except Exception as e:
            first = self.get_insert()

        try:
            # 類似文字説明を付与したデータに変換
            text = self.clipboard_get()
            insert_data_list = self.text_to_insert_data_list(text)

            for insert_data in insert_data_list:
                self.insert(first, *insert_data)

                # 挿入位置の更新
                for character in insert_data.chars:
                    if character == "\n":
                        first.row += 1
                        first.column = 0
                    else:
                        first.column += 1
        except Exception as e:
            pass

        return "break"

    def on_cut(self, event:tk.Event) -> str:
        """切り取り

        Args:
            event (tk.Event): イベントプロパティ

        Returns:
            str: "break"
        """
        try:
            first, last = self.get_sel()

            # 選択範囲の文字情報リストを取得
            character_data_list = self.get_character_data_list()
            character_data_list = character_data_list[self.row_n_column_to_index(character_data_list, *first):self.row_n_column_to_index(character_data_list, *last)]

            # 選択範囲から類似文字説明を除いたテキストを作成
            text = "".join((character_data.character for character_data in character_data_list if character_data.ctype is not CharacterType.EXPLAIN))

            # 選択範囲を削除
            self.delete(first, last)

            self.clipboard_clear()
            self.clipboard_append(text)
        except Exception as e:
            # 全て切り取り
            if len((text:=self.get_text())) > 0:
                text = text[:-1]  # 末尾の隠れ改行文字は要らない

            self.delete("1.0", END)

            self.clipboard_clear()
            self.clipboard_append(text)

        return "break"

    def on_backspace(self, event:tk.Event) -> str:
        """削除

        Args:
            event (tk.Event): イベントプロパティ

        Returns:
            str: "break"
        """
        character_data_list = self.get_character_data_list()

        try:
            first, last = self.get_sel()
        except Exception as e:
            last = self.get_insert()
            first = IndexData(*character_data_list[index]) if (index:=self.row_n_column_to_index(character_data_list, *last) - 1) >= 0 else None

        if first is not None and character_data_list[(index:=self.row_n_column_to_index(character_data_list, *first))].ctype is CharacterType.EXPLAIN:
            # 類似文字の先頭に移動
            first = IndexData(*max((character_data for character_data in character_data_list[:index] if character_data.ctype is CharacterType.SIMILAR)))

        if character_data_list[(index:=self.row_n_column_to_index(character_data_list, *last))].ctype is not CharacterType.DEFAULT:
            # 類似文字説明の末尾に移動
            last = IndexData(*min((character_data for character_data in character_data_list[index:] if character_data.ctype is not CharacterType.EXPLAIN)))

        if first is not None:
            self.delete(first, last)

        return "break"

    def on_delete(self, event:tk.Event) -> str:
        """削除

        Args:
            event (tk.Event): イベントプロパティ

        Returns:
            str: "break"
        """
        character_data_list = self.get_character_data_list()

        try:
            first, last = self.get_sel()
        except Exception as e:
            first = self.get_insert()
            last = IndexData(*character_data_list[index]) if (index:=self.row_n_column_to_index(character_data_list, *first) + 1) < len(character_data_list) else None

        if character_data_list[(index:=self.row_n_column_to_index(character_data_list, *first))].ctype is CharacterType.EXPLAIN:
            # 類似文字の先頭に移動
            first = IndexData(*max((character_data for character_data in character_data_list[:index] if character_data.ctype is CharacterType.SIMILAR)))

        if last is not None and character_data_list[(index:=self.row_n_column_to_index(character_data_list, *last))].ctype is not CharacterType.DEFAULT:
            # 類似文字説明の末尾に移動
            last = IndexData(*min((character_data for character_data in character_data_list[index:] if character_data.ctype is not CharacterType.EXPLAIN)))

        self.delete(first, last)

        return "break"

    def on_key_press(self, event:tk.Event) -> None:
        """キーを押した

        Args:
            event (tk.Event): イベントプロパティ
        """
        # 以下のキーコードはカーソル位置の強制移動なし
        if event.keycode in (
              8,  # BackSpace
             16,  # Shift
             #17,  # Ctrl コピー処理で使う
             18,  # Alt
             37,  # Arrow (Left)
             38,  # Arrow (Up)
             39,  # Arrow (Right)
             40,  # Arrow (Down)
             91,  # Windows
             93,  # Application
            112,  # F1
            113,  # F2
            114,  # F3
            115,  # F4
            116,  # F5
            117,  # F6
            118,  # F7
            119,  # F8
            120,  # F9
            121,  # F10
            122,  # F11
            123,  # F12
            144,  # NumLock
        ):
            return

        character_data_list = self.get_character_data_list()

        try:
            first, last, is_update = *self.get_sel(), False

            if character_data_list[(index:=self.row_n_column_to_index(character_data_list, *first))].ctype is CharacterType.EXPLAIN:
                # 類似文字説明の末尾に移動
                first, is_update = IndexData(*min((character_data for character_data in character_data_list[index:] if character_data.ctype is not CharacterType.EXPLAIN))), True

            if character_data_list[(index:=self.row_n_column_to_index(character_data_list, *last))].ctype is CharacterType.EXPLAIN:
                # 類似文字説明の末尾に移動
                last, is_update = IndexData(*min((character_data for character_data in character_data_list[index:] if character_data.ctype is not CharacterType.EXPLAIN))), True

            if is_update:
                # カーソル位置の更新
                self.mark_set(INSERT, last)
                # 選択範囲の更新
                self.tag_remove(SEL, "1.0", END)
                self.tag_add(SEL, first, last)

        except Exception as e:
            first = self.get_insert()

            if character_data_list[(index:=self.row_n_column_to_index(character_data_list, *first))].ctype is CharacterType.EXPLAIN:
                # 類似文字説明の末尾に移動
                first = IndexData(*min((character_data for character_data in character_data_list[index:] if character_data.ctype is not CharacterType.EXPLAIN)))
                # カーソル位置の移動
                self.mark_set(INSERT, first)

    def on_key_release(self, event:tk.Event) -> None:
        """キーを離した

        Args:
            event (tk.Event): イベントプロパティ
        """
        # 以下のキーコードは類似文字説明の挿入なし
        if event.keycode in (
              8,  # BackSpace
             16,  # Shift
             17,  # Ctrl
             18,  # Alt
             37,  # Arrow (Left)
             38,  # Arrow (Up)
             39,  # Arrow (Right)
             40,  # Arrow (Down)
             91,  # Windows
             93,  # Application
            112,  # F1
            113,  # F2
            114,  # F3
            115,  # F4
            116,  # F5
            117,  # F6
            118,  # F7
            119,  # F8
            120,  # F9
            121,  # F10
            122,  # F11
            123,  # F12
            144,  # NumLock
            229,  # 日本語入力の途中、未確定状態
        ):
            return

        # 類似文字の説明を除いたテキストを取得
        text = self.get_text(index2=INSERT)

        # 類似文字の説明を付与したデータリストを作成
        insert_data_list = self.text_to_insert_data_list(text)

        # 挿入位置までのテキストを削除
        self.delete("1.0", INSERT)

        # テキストの再挿入
        for insert_data in insert_data_list:
            self.insert(INSERT, *insert_data)

    def select_range(self, *args, **kwargs) -> None:
        """全選択した場合に呼ばれる
        """
        self.tag_add(SEL, "1.0", END)
        self.mark_set(INSERT, "1.0")
        self.see(INSERT)

    def icursor(self, *args, **kwargs) -> None:
        """select_rangeの後に呼ばれる
        """
        pass

    def set_text(self, text:str) -> None:
        """テキストをセット

        Args:
            text (str): テキスト
        """
        # 類似文字の説明を付与したデータリストを作成
        insert_data_list = self.text_to_insert_data_list(text)

        # 現在のテキストを全削除
        self.delete("1.0", END)

        # テキストの入れ替え
        for insert_data in insert_data_list:
            self.insert(INSERT, *insert_data)

    def get_sel_first(self) -> IndexData:
        """範囲選択の先頭の位置を取得

        範囲選択をしていない場合は例外が発生します。

        Raises:
            tk.TclError: not found 'SEL_FIRST'

        Returns:
            IndexData: 範囲選択の先頭の位置
        """
        return IndexData.from_index(self.index(SEL_FIRST))

    def get_sel_last(self) -> IndexData:
        """範囲選択の末尾の位置を取得

        範囲選択をしていない場合は例外が発生します。

        Raises:
            tk.TclError: not found 'SEL_LAST'

        Returns:
            IndexData: 範囲選択の末尾の位置
        """
        return IndexData.from_index(self.index(SEL_LAST))

    def get_insert(self) -> IndexData:
        """選択中の文字の位置を取得

        Returns:
            IndexData: 選択中の文字の位置データ
        """
        return IndexData.from_index(self.index(INSERT))

    def get_sel(self) -> tuple[IndexData, IndexData]:
        """範囲選択の先頭と末尾を取得

        範囲選択をしていない場合は例外が発生します。

        Raises:
            tk.TclError: not found 'SEL_FIRST' or 'SEL_LAST'

        Returns:
            tuple[IndexData, IndexData]: 範囲選択の先頭と末尾
        """
        return self.get_sel_first(), self.get_sel_last()

    def get_character_data_list(self) -> list[CharacterData]:
        """文字情報をリストで取得

        Returns:
            list[CharacterData]: 文字情報リスト
        """
        text = self.get_text()

        character_data_list:list[CharacterData] = []

        while len(text) > 0:
            index, similar_character, explain = self.find_similar_character(text)

            if index != -1:
                for character in text[:index]:
                    row = (character_data_list[-1].row if len(character_data_list) > 0 else 1) + (1 if len(character_data_list) > 0 and character_data_list[-1].character == "\n" else 0)
                    column = (character_data_list[-1].column + 1 if len(character_data_list) > 0 and character_data_list[-1].character != "\n" else 0)
                    character_data_list.append(CharacterData(index=len(character_data_list), row=row, column=column, character=character, ctype=CharacterType.DEFAULT))

                for character in similar_character:
                    row = (character_data_list[-1].row if len(character_data_list) > 0 else 1) + (1 if len(character_data_list) > 0 and character_data_list[-1].character == "\n" else 0)
                    column = (character_data_list[-1].column + 1 if len(character_data_list) > 0 and character_data_list[-1].character != "\n" else 0)
                    character_data_list.append(CharacterData(index=len(character_data_list), row=row, column=column, character=character, ctype=CharacterType.SIMILAR))

                for character in explain:
                    row = (character_data_list[-1].row if len(character_data_list) > 0 else 1) + (1 if len(character_data_list) > 0 and character_data_list[-1].character == "\n" else 0)
                    column = (character_data_list[-1].column + 1 if len(character_data_list) > 0 and character_data_list[-1].character != "\n" else 0)
                    character_data_list.append(CharacterData(index=len(character_data_list), row=row, column=column, character=character, ctype=CharacterType.EXPLAIN))

                text = text[index + len(similar_character):]
            else:
                for character in text:
                    row = (character_data_list[-1].row if len(character_data_list) > 0 else 1) + (1 if len(character_data_list) > 0 and character_data_list[-1].character == "\n" else 0)
                    column = (character_data_list[-1].column + 1 if len(character_data_list) > 0 and character_data_list[-1].character != "\n" else 0)
                    character_data_list.append(CharacterData(index=len(character_data_list), row=row, column=column, character=character, ctype=CharacterType.DEFAULT))
                break

        return character_data_list

    def row_n_column_to_index(self, character_data_list:list[CharacterData], row:int, column:int) -> int:
        """行列からインデックスに変換

        Args:
            character_data_list (list[CharacterData]): 文字情報リスト
            row (int): 行位置
            column (int): 列位置

        Returns:
            int: インデックス
        """
        for character_data in character_data_list:
            if character_data.row == row and character_data.column == column:
                return character_data.index
        return -1

    def text_to_insert_data_list(self, text:str) -> list[InsertData]:
        """分類文字の説明を除いたテキスト から insert関数に突っ込むデータリスト に変換

        Args:
            text (str): 分類文字の説明を除いたテキスト

        Returns:
            list[InsertData]: insert関数に突っ込むデータリスト
        """
        insert_data_list:list[InsertData] = []

        while len(text) > 0:
            index, similar_character, explain = self.find_similar_character(text)

            if index != -1:
                insert_data_list.append(InsertData(text[:index], CharacterType.DEFAULT))
                insert_data_list.append(InsertData(text[index:index + len(similar_character)], CharacterType.SIMILAR))
                insert_data_list.append(InsertData(explain, CharacterType.EXPLAIN))
                text = text[index + 1:]
            else:
                insert_data_list.append(InsertData(text, CharacterType.DEFAULT))
                break

        return insert_data_list

    def get_display_text(self, index1:str = "1.0", index2:str = END) -> str:
        """分類文字の説明を含むテキストを取得

        Args:
            index1 (str, optional): INDEX1. Defaults to "1.0".
            index2 (str, optional): INDEX2. Defaults to END.

        Returns:
            str: 分類文字の説明を含むテキスト
        """
        return self.get(index1, index2)

    def display_text_to_text(self, display_text:str) -> str:
        """分類文字の説明を含むテキスト から 分類文字の説明 を取り除きます。

        Args:
            display_text (str): 分類文字の説明を含むテキスト

        Returns:
            str: 分類文字の説明を除いたテキスト
        """
        text = ""

        while len(display_text) > 0:
            index, similar_character, explain = self.find_similar_character(display_text)

            if index != -1:
                text += display_text[:index + len(similar_character)]
                display_text = display_text[index + len(similar_character) + len(explain):]
            else:
                text += display_text
                break

        return text

    def get_text(self, index1:str = "1.0", index2:str = END) -> str:
        """分類文字の説明を除いたテキストを取得

        Args:
            index1 (str, optional): INDEX1. Defaults to "1.0".
            index2 (str, optional): INDEX2. Defaults to END.

        Returns:
            str: 分類文字の説明を除いたテキスト
        """
        return self.display_text_to_text(self.get_display_text(index1, index2))

    def find_similar_character(self, text:str) -> tuple[int, str, str]:
        """文字列から類似文字を探す

        文字列に類似文字が含まれない場合は、類似文字の位置は(-1)になります。

        Args:
            text (str): テキスト

        Returns:
            tuple[int, str, str]: 類似文字の位置, 見つかった類似文字, 見つかった類似文字の説明
        """
        # NOTE: 長い文字列の場合は速い
        # out_index, out_cln_char, out_tooltip = -1, "", ""
        # for cln_char, tooltip in self.similar_character_and_explain_table.items():
        #     if (index:=text.find(cln_char)) != -1 and (out_index == -1 or index < out_index):
        #         out_index, out_cln_char, out_tooltip = index, cln_char, tooltip
        # return out_index, out_cln_char, out_tooltip

        # NOTE: 短い文字列の場合は速い, 文字列は切り取って徐々に短くなるのでこっち
        for index, character in enumerate(text):
            if (explain:=self.similar_character_and_explain_table.get(character)) is not None:
                return index, character, explain

        return -1, "", ""
